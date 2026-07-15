import argparse
import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _by_from_string(by: str):
    by = (by or "css").lower()
    if by == "css":
        return By.CSS_SELECTOR
    if by == "xpath":
        return By.XPATH
    if by == "id":
        return By.ID
    if by == "name":
        return By.NAME
    if by == "text":
        # Not a native locator; handled separately
        return None
    return By.CSS_SELECTOR


def _wait_and_find(driver, selector: str, by: str, timeout: int):
    if by == "text":
        # Find element containing exact visible text
        xpath = f"//*[normalize-space(text())='{selector}']"
        return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    locator_by = _by_from_string(by)
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((locator_by, selector)))


def _expand_env_vars(value: str) -> str:
    """Replace ${VAR} with environment variable values."""
    if not isinstance(value, str):
        return value
    import re
    # First pass: ${VAR}
    def repl1(match):
        var = match.group(1)
        return os.getenv(var, match.group(0))
    s = re.sub(r"\$\{([^}]+)\}", repl1, value)
    # Second pass: $VAR
    def repl2(match):
        var = match.group(1)
        return os.getenv(var, match.group(0))
    s = re.sub(r"\$([A-Za-z_][A-Za-z0-9_]*)", repl2, s)
    return s


def perform_actions(driver, actions: list):
    """Perform a sequence of UI actions described in config."""
    for idx, action in enumerate(actions or []):
        atype = (action.get("type") or "").lower()
        by = action.get("by", "css")
        selector = action.get("selector")
        timeout = int(action.get("timeout", 20))
        try:
            if atype == "click":
                el = _wait_and_find(driver, selector, by, timeout)
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                driver.execute_script("arguments[0].click();", el)
            elif atype == "type":
                el = _wait_and_find(driver, selector, by, timeout)
                if action.get("clear", True):
                    el.clear()
                text = _expand_env_vars(action.get("text", ""))
                el.send_keys(text)
            elif atype == "wait":
                # wait for element visible but no action
                _ = WebDriverWait(driver, timeout).until(
                    EC.visibility_of_element_located((_by_from_string(by), selector))
                )
            elif atype == "wait_url_contains":
                substr = action.get("text") or action.get("substring") or ""
                WebDriverWait(driver, timeout).until(lambda d: substr in d.current_url)
            elif atype == "sleep":
                time.sleep(float(action.get("seconds", 1)))
            elif atype == "js":
                driver.execute_script(action.get("script", ""))
            elif atype == "scroll":
                driver.execute_script(f"window.scrollTo(0, {int(action.get('y', 0))});")
            else:
                print(f"⚠️ Unknown action type: {atype} (skipped)")
        except Exception as e:
            raise RuntimeError(f"Action #{idx+1} failed ({atype} {selector}): {e}")


def capture_pdf(config_path: Path, output_dir: Path):
    # Load environment variables from project .env if present
    try:
        env_path = Path(__file__).resolve().parents[1] / ".env"
        load_dotenv(dotenv_path=env_path)
    except Exception:
        pass
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))

    url = cfg.get("url")
    actions = cfg.get("actions", [])
    pdf_opts = cfg.get("pdf", {})
    capture_opts = cfg.get("capture", {})

    if not url:
        raise ValueError("Config must include 'url'")

    output_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")

    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        time.sleep(float(cfg.get("initialSleep", 2)))

        # Optional: emulate high-DPI/viewport for sharper screenshots
        try:
            dpr = int(capture_opts.get("deviceScaleFactor", 0))
            vp_w = int(capture_opts.get("viewportWidth", 0))
            vp_h = int(capture_opts.get("viewportHeight", 0))
            if dpr or vp_w or vp_h:
                if not vp_w:
                    vp_w = driver.execute_script("return window.innerWidth;")
                if not vp_h:
                    vp_h = driver.execute_script("return window.innerHeight;")
                if not dpr:
                    dpr = driver.execute_script("return window.devicePixelRatio;")
                driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
                    'width': vp_w,
                    'height': vp_h,
                    'deviceScaleFactor': dpr,
                    'mobile': False
                })
        except Exception:
            pass

        # Perform actions (login, cookie accept, navigation, etc.)
        perform_actions(driver, actions)

        # Optional: wait until DOM height stabilizes after navigation
        def wait_dom_stability(max_seconds: float, interval: float = 0.5, stable_window: float = 1.5):
            if max_seconds <= 0:
                return
            start = time.perf_counter()
            last_height = None
            last_change = start
            while True:
                now = time.perf_counter()
                if now - start > max_seconds:
                    break
                height = driver.execute_script(
                    "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);"
                )
                if height != last_height:
                    last_height = height
                    last_change = now
                # If height unchanged for stable_window seconds, consider DOM stable
                if (now - last_change) >= stable_window:
                    break
                time.sleep(interval)

        wait_dom_stability(float(cfg.get("domStableWaitSeconds", 0)))

        # Optional: full scroll to bottom to trigger lazy loading
        if bool(capture_opts.get("preCaptureFullScroll", False)):
            try:
                print("🔄 Starting full-page scroll to load all content...")
                start_t = time.perf_counter()
                max_s = float(capture_opts.get("fullScrollWaitSeconds", 10.0))
                step_ms = float(capture_opts.get("scrollIntervalMs", 250.0))
                passes = int(capture_opts.get("scrollPasses", 2))
                
                for pass_num in range(passes):
                    print(f"  Pass {pass_num+1}/{passes}...")
                    driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(0.5)
                    
                    while time.perf_counter() - start_t < max_s:
                        prev_h = driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);")
                        driver.execute_script("window.scrollBy(0, window.innerHeight / 2);")
                        time.sleep(step_ms/1000.0)
                        
                        y = driver.execute_script("return window.scrollY + window.innerHeight;")
                        h = driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);")
                        
                        if y >= h - 10:
                            print(f"    Reached bottom: scrollY={y:.0f}, scrollHeight={h:.0f}")
                            time.sleep(1.0)
                            # Check if height expanded
                            new_h = driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);")
                            if new_h > h:
                                print(f"    Height expanded: {h:.0f} → {new_h:.0f}")
                                h = new_h
                            else:
                                break
                
                # Re-apply overflow fix after scroll
                if bool(pdf_opts.get("forceRemoveOverflow", False)):
                    driver.execute_script(
                        """
                        document.documentElement.style.overflow = 'visible';
                        document.body.style.overflow = 'visible';
                        var els = document.querySelectorAll('*');
                        els.forEach(function(el){
                            var cs = getComputedStyle(el);
                            if (cs && (cs.overflowY==='auto' || cs.overflowY==='scroll' || cs.overflowY==='hidden')) {
                                el.style.overflowY='visible';
                                el.style.maxHeight='none';
                                if (cs.height && cs.height!=='auto') {
                                    el.style.height='auto';
                                }
                            }
                        });
                        """
                    )
                    time.sleep(0.5)
                
                # After reaching bottom, wait for final stability and scroll back to top
                print("  Waiting for final DOM stability...")
                wait_dom_stability(float(capture_opts.get("postScrollStableWaitSeconds", 3.0)))
                driver.execute_script("window.scrollTo(0,0);")
                time.sleep(1.0)
                
                # Force reflow
                final_h = driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);")
                print(f"✅ Final page height: {final_h}px ({final_h/96:.1f} inches)")
            except Exception as e:
                print(f"⚠️ Scroll error: {e}")

        # Optional: disable links
        if bool(pdf_opts.get("disableLinks", True)):
            driver.execute_script("""
                var links = document.querySelectorAll('a');
                links.forEach(function(link) {
                    link.removeAttribute('href');
                    link.style.cursor = 'text';
                });
            """)
            time.sleep(0.2)

        # Optional: inject custom CSS before printing/screenshot to expand containers
        inject_css = pdf_opts.get("injectCss")
        if inject_css:
            driver.execute_script(
                """
                (function(css){
                    var style = document.createElement('style');
                    style.setAttribute('data-injected','print-css');
                    style.type='text/css';
                    style.appendChild(document.createTextNode(css));
                    document.head.appendChild(style);
                })(arguments[0]);
                """,
                inject_css
            )
            time.sleep(0.2)

        # Optional: force remove overflow on scrollable containers (generic)
        if bool(pdf_opts.get("forceRemoveOverflow", False)):
            driver.execute_script(
                """
                document.documentElement.style.overflow = 'visible';
                document.body.style.overflow = 'visible';
                var els = document.querySelectorAll('*');
                els.forEach(function(el){
                    var cs = getComputedStyle(el);
                    if (cs && (cs.overflowY==='auto' || cs.overflowY==='scroll' || cs.overflowY==='hidden')) {
                        el.style.overflowY='visible';
                        el.style.maxHeight='none';
                        if (cs.height && cs.height!=='auto') {
                            el.style.height='auto';
                        }
                    }
                });
                """
            )
            time.sleep(0.2)

        # Scroll to top before capture
        driver.execute_script("window.scrollTo(0,0);")
        time.sleep(0.5)

        # Screenshot using viewport stitching (no height limits)
        import base64
        from PIL import Image
        import io
        
        print("📸 Capturing full page via viewport stitching...")
        
        # Get dimensions
        total_width = driver.execute_script("return Math.max(document.body.scrollWidth, document.documentElement.scrollWidth, document.body.offsetWidth, document.documentElement.offsetWidth, document.body.clientWidth, document.documentElement.clientWidth);")
        total_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight, document.documentElement.offsetHeight, document.body.clientHeight, document.documentElement.clientHeight);")
        viewport_width = driver.execute_script("return window.innerWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        
        print(f"  Page: {total_width}×{total_height}px, Viewport: {viewport_width}×{viewport_height}px")
        
        # Calculate device pixel ratio
        dpr = driver.execute_script("return window.devicePixelRatio")
        
        # Create canvas for full page
        stitched = Image.new('RGB', (int(total_width * dpr), int(total_height * dpr)))
        
        # Capture viewport by viewport
        offset = 0
        capture_count = 0
        while offset < total_height:
            driver.execute_script(f"window.scrollTo(0, {offset});")
            time.sleep(0.3)
            
            # Capture current viewport
            screenshot = driver.get_screenshot_as_png()
            img = Image.open(io.BytesIO(screenshot))
            
            # Paste into stitched image
            y_pos = int(offset * dpr)
            stitched.paste(img, (0, y_pos))
            
            capture_count += 1
            offset += viewport_height
            
            if capture_count % 5 == 0:
                print(f"  Captured {capture_count} viewports ({offset}/{total_height}px)...")
        
        print(f"  ✅ Stitched {capture_count} viewports")
        
        # Save stitched screenshot
        png_path = output_dir / f"capture_{ts}.png"
        stitched.save(png_path, 'PNG', optimize=False)
        print(f"  Saved: {stitched.width}×{stitched.height}px")
        
        # Scroll back to top
        driver.execute_script("window.scrollTo(0,0);")
        time.sleep(0.3)

        # Emulate print media if requested (can improve copyable layout)
        if bool(pdf_opts.get("emulatePrintMedia", False)):
            try:
                driver.execute_cdp_cmd('Emulation.setEmulatedMedia', { 'media': 'print' })
            except Exception:
                pass

        # Print to PDF with copyable text (native mode)
        # Use EXACT dimensions from the stitched screenshot to match perfectly
        fit_to_content = bool(pdf_opts.get("fitToContent", True))
        scale = float(pdf_opts.get("scale", 1.0))
        margins = pdf_opts.get("margins", {"top":0, "bottom":0, "left":0, "right":0})
        dual_output = bool(pdf_opts.get("dualOutput", False))
        mode = (pdf_opts.get("mode") or "native").lower()

        # Get exact dimensions from stitched image
        actual_width_px = stitched.width / dpr
        actual_height_px = stitched.height / dpr
        paper_width = actual_width_px / 96.0
        paper_height = actual_height_px / 96.0
        
        print(f"📄 PDF paper size: {paper_width:.2f} × {paper_height:.2f} inches (matches screenshot)")
        
        # Safeguard: cap height to max to avoid Chrome truncation
        max_h = float(pdf_opts.get('maxPaperHeight', 200.0))
        if paper_height > max_h:
            print(f"⚠️ Native PDF height {paper_height:.2f}in exceeds max {max_h}in; capping to avoid truncation.")
            paper_height = max_h

        result = driver.execute_cdp_cmd('Page.printToPDF', {
            'printBackground': True,
            'displayHeaderFooter': False,
            'paperWidth': paper_width,
            'paperHeight': paper_height,
            'marginTop': float(margins.get('top', 0)),
            'marginBottom': float(margins.get('bottom', 0)),
            'marginLeft': float(margins.get('left', 0)),
            'marginRight': float(margins.get('right', 0)),
            'scale': scale,
            'preferCSSPageSize': bool(pdf_opts.get('preferCSSPageSize', False))
        })

        pdf_path = output_dir / f"capture_{ts}.pdf"
        with open(pdf_path, 'wb') as f:
            f.write(base64.b64decode(result['data']))

        # Optional: image-based PDF for maximum visual fidelity
        if dual_output or mode == 'image':
            try:
                from PIL import Image
                from reportlab.pdfgen import canvas
                from reportlab.lib.units import inch
                img = Image.open(png_path)
                px_w, px_h = img.size
                # Convert pixels to points via 96 DPI -> inches -> points
                in_w = px_w / 96.0
                in_h = px_h / 96.0
                page_w = in_w * 72.0
                page_h = in_h * 72.0
                img_pdf_path = output_dir / f"capture_{ts}_image.pdf"
                c = canvas.Canvas(str(img_pdf_path), pagesize=(page_w, page_h))
                # Draw image to fill page
                c.drawImage(str(png_path), 0, 0, width=page_w, height=page_h)
                c.showPage()
                c.save()
                print(f"✅ Image-PDF saved: {img_pdf_path}")
            except Exception as e:
                print(f"⚠️ Image-PDF generation skipped: {e}")

        print(f"✅ PDF saved: {pdf_path}")
        print(f"✅ PNG saved: {png_path}")
        return str(pdf_path)
    finally:
        driver.quit()


def main():
    parser = argparse.ArgumentParser(description="Capture a web page to PDF with configurable actions")
    parser.add_argument('--config', required=True, help='Path to JSON config file')
    parser.add_argument('--outdir', default='outputs/pdf', help='Directory to save PDF and PNG')
    args = parser.parse_args()

    capture_pdf(Path(args.config), Path(args.outdir))


if __name__ == '__main__':
    main()
