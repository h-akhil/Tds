# add imports near top
import io, base64, re
import pdfplumber
import pandas as pd
from urllib.parse import urljoin

def download_url_content(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.content

def compute_answer_for_page(page):
    try:
        # 1) JSON embedded in <pre>
        pre = page.query_selector("pre")
        if pre:
            try:
                j = json.loads(pre.inner_text())
                if "answer" in j:
                    return j["answer"]
                if j.get("url"):
                    content = download_url_content(urljoin(page.url, j["url"]))
                    # fallthrough to PDF handling below
            except Exception:
                pass

        # 2) PDF links on page -> try pdfplumber on page 2
        for a in page.query_selector_all("a"):
            href = a.get_attribute("href") or ""
            if href.lower().endswith(".pdf"):
                content = download_url_content(urljoin(page.url, href))
                with pdfplumber.open(io.BytesIO(content)) as pdf:
                    if len(pdf.pages) > 1:
                        tables = pdf.pages[1].extract_tables() or []
                        if tables:
                            df = pd.DataFrame(tables[0][1:], columns=tables[0][0])
                            # try to find a column named 'value' (case-insensitive)
                            cols = {c.lower(): c for c in df.columns}
                            if "value" in cols:
                                col = cols["value"]
                                s = pd.to_numeric(df[col], errors="coerce").sum()
                                if abs(s - round(s)) < 1e-9:
                                    return int(round(s))
                                return float(s)
        # 3) fallback: sum all numbers in any HTML table on the page
        for t in page.query_selector_all("table"):
            html = t.inner_html()
            nums = re.findall(r"[-+]?\d*\.\d+|\d+", html)
            if nums:
                s = sum(float(x) for x in nums)
                if abs(s - round(s)) < 1e-9:
                    return int(round(s))
                return s
    except Exception as e:
        print("compute_answer error:", e)
    return {"note":"no-answer-found"}
