from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>64-bit Three-Level Paging Simulation</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:      #f8f8f6;
    --surface: #ffffff;
    --border:  #dddbd4;
    --text:    #1a1a18;
    --muted:   #6b6b67;
    --hint:    #9b9b97;

    --p50:#EEEDFE; --p100:#CECBF6; --p400:#7F77DD; --p600:#534AB7; --p800:#3C3489;
    --t50:#E1F5EE; --t100:#9FE1CB; --t400:#1D9E75; --t600:#0F6E56; --t800:#085041;
    --a50:#FAEEDA; --a100:#FAC775; --a400:#BA7517; --a600:#854F0B; --a800:#633806;
    --c50:#FAECE7; --c100:#F5C4B3; --c400:#D85A30; --c600:#993C1D; --c800:#712B13;
    --g50:#F1EFE8; --g200:#B4B2A9; --g400:#888780; --g600:#5F5E5A; --g800:#444441;
    --bl50:#E6F1FB; --bl100:#B5D4F4; --bl400:#378ADD; --bl600:#185FA5; --bl800:#0C447C;
    --gr50:#EAF3DE; --gr100:#C0DD97; --gr600:#3B6D11; --gr800:#27500A;
  }

  @media (prefers-color-scheme: dark) {
    :root {
      --bg:      #1a1a18;
      --surface: #242422;
      --border:  #3a3a36;
      --text:    #e8e8e2;
      --muted:   #9b9b97;
      --hint:    #6b6b67;

      --p50:#26215C; --p100:#3C3489; --p400:#AFA9EC; --p600:#CECBF6; --p800:#EEEDFE;
      --t50:#04342C; --t100:#085041; --t400:#5DCAA5; --t600:#9FE1CB; --t800:#E1F5EE;
      --a50:#412402; --a100:#633806; --a400:#EF9F27; --a600:#FAC775; --a800:#FAEEDA;
      --c50:#4A1B0C; --c100:#712B13; --c400:#F0997B; --c600:#F5C4B3; --c800:#FAECE7;
      --g50:#2C2C2A; --g200:#5F5E5A; --g400:#888780; --g600:#B4B2A9; --g800:#D3D1C7;
      --bl50:#042C53; --bl100:#0C447C; --bl400:#85B7EB; --bl600:#B5D4F4; --bl800:#E6F1FB;
      --gr50:#173404; --gr100:#27500A; --gr600:#97C459; --gr800:#C0DD97;
    }
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 14px;
    line-height: 1.6;
    padding: 24px 16px;
  }

  .container { max-width: 900px; margin: 0 auto; }

  h1 { font-size: 20px; font-weight: 600; margin-bottom: 4px; }
  .subtitle { font-size: 13px; color: var(--muted); margin-bottom: 24px; }

  .card {
    background: var(--surface);
    border: 0.5px solid var(--border);
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 14px;
  }
  .card-title {
    font-size: 12px;
    font-weight: 500;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .06em;
    margin-bottom: 12px;
  }

  /* ── ADDRESS BAR ── */
  .addr-strip {
    display: flex;
    width: 100%;
    border-radius: 8px;
    overflow: hidden;
    border: 0.5px solid var(--border);
    height: 40px;
    cursor: pointer;
  }
  .aseg {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 600;
    transition: filter .15s;
    user-select: none;
  }
  .aseg:hover { filter: brightness(.92); }
  .aseg.hl   { outline: 3px solid var(--bl400); outline-offset: -2px; z-index: 1; }

  .aseg.res { background: var(--g50);  color: var(--g800);  flex: 16; }
  .aseg.l1  { background: var(--p50);  color: var(--p800);  flex:  9; }
  .aseg.l2  { background: var(--t50);  color: var(--t800);  flex:  9; }
  .aseg.l3  { background: var(--a50);  color: var(--a800);  flex:  9; }
  .aseg.off { background: var(--c50);  color: var(--c800);  flex: 21; }

  .ruler {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: var(--hint);
    margin-top: 4px;
    margin-bottom: 10px;
    padding: 0 2px;
  }

  /* Legend */
  .legend { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px; }
  .lpill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    padding: 3px 9px;
    border-radius: 20px;
    cursor: pointer;
    border: 0.5px solid transparent;
    background: var(--bg);
  }
  .lpill:hover { border-color: var(--border); }
  .ldot { width: 9px; height: 9px; border-radius: 2px; flex-shrink: 0; }
  .lpill.res .ldot { background: var(--g600); }
  .lpill.l1  .ldot { background: var(--p600); }
  .lpill.l2  .ldot { background: var(--t600); }
  .lpill.l3  .ldot { background: var(--a600); }
  .lpill.off .ldot { background: var(--c600); }

  /* Info box */
  .infobox {
    background: var(--bg);
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    color: var(--muted);
    min-height: 38px;
    line-height: 1.7;
    border: 0.5px solid var(--border);
  }
  .infobox strong { color: var(--text); font-weight: 600; }

  /* ── CONTROLS ── */
  .ctrl-row {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 10px;
  }
  .ctrl-row label { font-size: 12px; color: var(--muted); white-space: nowrap; }
  input[type=number] {
    font-size: 13px;
    padding: 6px 10px;
    border-radius: 7px;
    border: 0.5px solid var(--border);
    background: var(--surface);
    color: var(--text);
    width: 200px;
    outline: none;
  }
  input[type=number]:focus { border-color: var(--bl400); }
  .hex-disp {
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 13px;
    color: var(--muted);
    letter-spacing: .04em;
  }

  .btn-row { display: flex; gap: 8px; flex-wrap: wrap; }
  .btn {
    padding: 7px 16px;
    border-radius: 7px;
    border: 0.5px solid var(--border);
    background: var(--surface);
    color: var(--text);
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: background .12s, border-color .12s;
  }
  .btn:hover { background: var(--bg); border-color: var(--g400); }
  .btn.primary {
    background: var(--bl50);
    color: var(--bl800);
    border-color: var(--bl400);
  }
  .btn.primary:hover { background: var(--bl100); }

  /* ── ANIMATION CANVAS ── */
  #walk-svg { width: 100%; display: block; }

  /* TLB row */
  .tlb-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding-top: 10px;
    flex-wrap: wrap;
  }
  .tlb-label { font-size: 12px; color: var(--muted); }
  .tlb-badge {
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 5px;
  }
  .tlb-hit  { background: var(--t50);  color: var(--t800); }
  .tlb-miss { background: var(--c50);  color: var(--c800); }

  /* Step log */
  .step-log {
    max-height: 160px;
    overflow-y: auto;
    background: var(--bg);
    border: 0.5px solid var(--border);
    border-radius: 8px;
    padding: 10px 12px;
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 11px;
    line-height: 1.9;
  }
  .log-entry { display: flex; gap: 8px; align-items: baseline; }
  .log-step  { color: var(--muted); min-width: 20px; }
  .log-l1    { color: var(--p600); }
  .log-l2    { color: var(--t600); }
  .log-l3    { color: var(--a600); }
  .log-off   { color: var(--c600); }
  .log-ok    { color: var(--gr600); }

  /* ── RESULT CHIPS ── */
  .chips {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
    gap: 10px;
  }
  .chip { border-radius: 9px; padding: 10px 13px; }
  .chip.l1   { background: var(--p50); }
  .chip.l2   { background: var(--t50); }
  .chip.l3   { background: var(--a50); }
  .chip.off  { background: var(--c50); }
  .chip.phys { background: var(--bl50); }
  .chip .cl  { font-size: 10px; font-weight: 600; margin-bottom: 3px; text-transform: uppercase; letter-spacing: .05em; }
  .chip.l1   .cl { color: var(--p800); }
  .chip.l2   .cl { color: var(--t800); }
  .chip.l3   .cl { color: var(--a800); }
  .chip.off  .cl { color: var(--c800); }
  .chip.phys .cl { color: var(--bl800); }
  .chip .cv  { font-family: "SFMono-Regular", Consolas, monospace; font-size: 13px; font-weight: 600; color: var(--text); }
  .chip .cs  { font-size: 10px; color: var(--muted); margin-top: 2px; }

  /* ── STATS ── */
  .stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 10px;
  }
  .stat { background: var(--bg); border-radius: 8px; padding: 10px 12px; }
  .stat .sl { font-size: 11px; color: var(--muted); margin-bottom: 2px; }
  .stat .sv { font-size: 17px; font-weight: 600; }

  /* animations */
  @keyframes flowDash { to { stroke-dashoffset: -24; } }
  @keyframes pulseRing { 0% { r: 5; opacity: 1; } 100% { r: 18; opacity: 0; } }
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  .flow-line { stroke-dasharray: 6 4; animation: flowDash .8s linear infinite; }
  .pulse-ring { animation: pulseRing .9s ease-out infinite; }
  .fade-in    { animation: fadeIn .3s ease; }

  /* speed control */
  .speed-row { display: flex; align-items: center; gap: 10px; }
  .speed-row label { font-size: 12px; color: var(--muted); }
  input[type=range] { flex: 1; max-width: 160px; accent-color: var(--bl400); }
</style>
</head>
<body>
<div class="container">

  <h1>64-bit Three-Level Paging Simulation</h1>
  <p class="subtitle">x86-64 style · 48-bit virtual address space · 3-level page tables · 2 MB pages</p>

  <!-- ADDRESS BAR -->
  <div class="card">
    <div class="card-title">Virtual address layout — click a segment</div>
    <div class="addr-strip" id="addr-strip">
      <div class="aseg res" data-seg="res" onclick="segClick('res')">Reserved</div>
      <div class="aseg l1"  data-seg="l1"  onclick="segClick('l1')">L1</div>
      <div class="aseg l2"  data-seg="l2"  onclick="segClick('l2')">L2</div>
      <div class="aseg l3"  data-seg="l3"  onclick="segClick('l3')">L3</div>
      <div class="aseg off" data-seg="off" onclick="segClick('off')">Offset</div>
    </div>
    <div class="ruler">
      <span>Bit 63</span><span>Bit 47</span><span>Bit 38</span>
      <span>Bit 29</span><span>Bit 20</span><span>Bit 0</span>
    </div>
    <div class="legend">
      <span class="lpill res" onclick="segClick('res')"><span class="ldot"></span>Reserved [63:48] — 16 bits</span>
      <span class="lpill l1"  onclick="segClick('l1')"><span class="ldot"></span>L1 / PGD [47:39] — 9 bits</span>
      <span class="lpill l2"  onclick="segClick('l2')"><span class="ldot"></span>L2 / PMD [38:30] — 9 bits</span>
      <span class="lpill l3"  onclick="segClick('l3')"><span class="ldot"></span>L3 / PTE [29:21] — 9 bits</span>
      <span class="lpill off" onclick="segClick('off')"><span class="ldot"></span>Page offset [20:0] — 21 bits → 2 MB page</span>
    </div>
    <div class="infobox" id="infobox">Click any colored segment above to learn what that field does during address translation.</div>
  </div>

  <!-- SYSTEM STATS -->
  <div class="card">
    <div class="card-title">System parameters</div>
    <div class="stats">
      <div class="stat"><div class="sl">VA bits total</div><div class="sv">64</div></div>
      <div class="stat"><div class="sl">Bits used</div><div class="sv">48</div></div>
      <div class="stat"><div class="sl">Page table levels</div><div class="sv">3</div></div>
      <div class="stat"><div class="sl">Entries / table</div><div class="sv">512</div></div>
      <div class="stat"><div class="sl">Entry size</div><div class="sv">8 B</div></div>
      <div class="stat"><div class="sl">Table size</div><div class="sv">4 KB</div></div>
      <div class="stat"><div class="sl">Page size</div><div class="sv">2 MB</div></div>
      <div class="stat"><div class="sl">VA space</div><div class="sv">256 TB</div></div>
    </div>
  </div>

  <!-- CONTROLS -->
  <div class="card">
    <div class="card-title">Enter a virtual address</div>
    <div class="ctrl-row">
      <label>Decimal</label>
      <input type="number" id="va-in" value="140737488355328" min="0">
      <span class="hex-disp" id="hex-out">0x0000800000000000</span>
    </div>
    <div class="btn-row" style="margin-bottom:10px">
      <button class="btn primary" onclick="runTranslate()">▶ Translate &amp; Animate</button>
      <button class="btn" onclick="randomAddr()">Random address</button>
      <button class="btn" onclick="presetAddr('user')">User space</button>
      <button class="btn" onclick="presetAddr('kernel')">Kernel space</button>
      <button class="btn" onclick="clearAll()">Reset</button>
    </div>
    <div class="speed-row">
      <label>Animation speed</label>
      <input type="range" id="speed" min="200" max="1500" step="100" value="750">
      <span id="speed-label" style="font-size:12px;color:var(--muted);min-width:60px">Medium</span>
    </div>
  </div>

  <!-- ANIMATED WALK -->
  <div class="card">
    <div class="card-title">Page table walk — animated</div>
    <svg id="walk-svg" viewBox="0 0 860 380" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5"
                markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"
                stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </marker>
      </defs>

      <!-- CR3 -->
      <rect x="10" y="30" width="100" height="52" rx="9"
            fill="var(--g50)" stroke="var(--g600)" stroke-width="0.5"/>
      <text x="60" y="50" text-anchor="middle" dominant-baseline="central"
            style="font-size:13px;font-weight:600;fill:var(--g800)">CR3</text>
      <text x="60" y="66" text-anchor="middle" dominant-baseline="central"
            style="font-size:10px;fill:var(--g600)" id="cr3-val">base=0x1000</text>

      <!-- L1 PGD -->
      <rect x="180" y="10" width="140" height="90" rx="9"
            fill="var(--p50)" stroke="var(--p600)" stroke-width="0.5"/>
      <text x="250" y="32" text-anchor="middle" dominant-baseline="central"
            style="font-size:13px;font-weight:600;fill:var(--p800)">L1 — PGD</text>
      <text x="250" y="50" text-anchor="middle" dominant-baseline="central"
            style="font-size:10px;fill:var(--p600)">512 entries × 8 B = 4 KB</text>
      <rect id="b-l1e" x="194" y="62" width="112" height="28" rx="5"
            fill="var(--p100)" stroke="var(--p400)" stroke-width="0.5"/>
      <text id="t-l1e" x="250" y="76" text-anchor="middle" dominant-baseline="central"
            style="font-size:11px;fill:var(--p800)">entry [?]</text>

      <!-- L2 PMD -->
      <rect x="380" y="10" width="140" height="90" rx="9"
            fill="var(--t50)" stroke="var(--t600)" stroke-width="0.5"/>
      <text x="450" y="32" text-anchor="middle" dominant-baseline="central"
            style="font-size:13px;font-weight:600;fill:var(--t800)">L2 — PMD</text>
      <text x="450" y="50" text-anchor="middle" dominant-baseline="central"
            style="font-size:10px;fill:var(--t600)">512 entries × 8 B = 4 KB</text>
      <rect id="b-l2e" x="394" y="62" width="112" height="28" rx="5"
            fill="var(--t100)" stroke="var(--t400)" stroke-width="0.5"/>
      <text id="t-l2e" x="450" y="76" text-anchor="middle" dominant-baseline="central"
            style="font-size:11px;fill:var(--t800)">entry [?]</text>

      <!-- L3 PTE -->
      <rect x="580" y="10" width="140" height="90" rx="9"
            fill="var(--a50)" stroke="var(--a600)" stroke-width="0.5"/>
      <text x="650" y="32" text-anchor="middle" dominant-baseline="central"
            style="font-size:13px;font-weight:600;fill:var(--a800)">L3 — PTE</text>
      <text x="650" y="50" text-anchor="middle" dominant-baseline="central"
            style="font-size:10px;fill:var(--a600)">512 entries × 8 B = 4 KB</text>
      <rect id="b-l3e" x="594" y="62" width="112" height="28" rx="5"
            fill="var(--a100)" stroke="var(--a400)" stroke-width="0.5"/>
      <text id="t-l3e" x="650" y="76" text-anchor="middle" dominant-baseline="central"
            style="font-size:11px;fill:var(--a800)">entry [?]</text>

      <!-- Physical frame -->
      <rect id="b-phys" x="500" y="230" width="200" height="70" rx="9"
            fill="var(--c50)" stroke="var(--c600)" stroke-width="0.5"/>
      <text x="600" y="257" text-anchor="middle" dominant-baseline="central"
            style="font-size:13px;font-weight:600;fill:var(--c800)">Physical Frame</text>
      <text id="t-phys" x="600" y="277" text-anchor="middle" dominant-baseline="central"
            style="font-size:10px;fill:var(--c600)">frame_base + offset</text>

      <!-- Offset box -->
      <rect x="160" y="230" width="180" height="70" rx="9"
            fill="var(--c50)" stroke="var(--c400)" stroke-width="0.5" stroke-dasharray="5 3"/>
      <text x="250" y="257" text-anchor="middle" dominant-baseline="central"
            style="font-size:13px;font-weight:600;fill:var(--c800)">Page Offset</text>
      <text id="t-off" x="250" y="277" text-anchor="middle" dominant-baseline="central"
            style="font-size:10px;fill:var(--c600)">21 bits direct</text>

      <!-- TLB box -->
      <rect id="b-tlb" x="700" y="220" width="140" height="90" rx="9"
            fill="var(--gr50)" stroke="var(--gr600)" stroke-width="0.5"/>
      <text x="770" y="248" text-anchor="middle" dominant-baseline="central"
            style="font-size:13px;font-weight:600;fill:var(--gr800)">TLB Cache</text>
      <text id="t-tlb" x="770" y="268" text-anchor="middle" dominant-baseline="central"
            style="font-size:10px;fill:var(--gr600)">Translation cache</text>
      <text id="t-tlb2" x="770" y="284" text-anchor="middle" dominant-baseline="central"
            style="font-size:10px;fill:var(--gr600)">—</text>

      <!-- Static dim guides -->
      <line x1="110" y1="56" x2="178" y2="56" stroke="var(--g200)" stroke-width="1" stroke-dasharray="3 3"/>
      <line x1="322" y1="56" x2="378" y2="56" stroke="var(--g200)" stroke-width="1" stroke-dasharray="3 3"/>
      <line x1="522" y1="56" x2="578" y2="56" stroke="var(--g200)" stroke-width="1" stroke-dasharray="3 3"/>
      <line x1="650" y1="100" x2="650" y2="180" stroke="var(--g200)" stroke-width="1" stroke-dasharray="3 3"/>
      <line x1="650" y1="180" x2="600" y2="228" stroke="var(--g200)" stroke-width="1" stroke-dasharray="3 3"/>
      <line x1="250" y1="230" x2="498" y2="262" stroke="var(--g200)" stroke-width="1" stroke-dasharray="3 3"/>

      <!-- Step labels -->
      <text x="144" y="44" text-anchor="middle" style="font-size:11px;fill:var(--muted)">① CR3</text>
      <text x="350" y="44" text-anchor="middle" style="font-size:11px;fill:var(--muted)">② L1[idx]</text>
      <text x="550" y="44" text-anchor="middle" style="font-size:11px;fill:var(--muted)">③ L2[idx]</text>

      <!-- Animated overlay -->
      <g id="anim-layer"></g>

      <!-- Status bar -->
      <rect x="0" y="350" width="860" height="30" rx="0" fill="var(--bg)" opacity="0.7"/>
      <text id="walk-status" x="430" y="365" text-anchor="middle" dominant-baseline="central"
            style="font-size:12px;fill:var(--muted)">Enter an address above and click Translate &amp; Animate</text>
    </svg>

    <!-- TLB indicator -->
    <div class="tlb-row">
      <span class="tlb-label">TLB lookup result:</span>
      <span class="tlb-badge" id="tlb-badge" style="display:none"></span>
      <span class="tlb-label" id="tlb-msg" style="font-style:italic">—</span>
    </div>
  </div>

  <!-- STEP LOG -->
  <div class="card">
    <div class="card-title">Step-by-step log</div>
    <div class="step-log" id="step-log">
      <div style="color:var(--hint);font-style:italic">Walk steps will appear here after translation…</div>
    </div>
  </div>

  <!-- RESULT CHIPS -->
  <div class="card">
    <div class="card-title">Decomposed address fields</div>
    <div class="chips" id="chips">
      <div class="chip l1">
        <div class="cl">L1 index (PGD)</div>
        <div class="cv" id="r-l1">—</div>
        <div class="cs">bits [47:39]</div>
      </div>
      <div class="chip l2">
        <div class="cl">L2 index (PMD)</div>
        <div class="cv" id="r-l2">—</div>
        <div class="cs">bits [38:30]</div>
      </div>
      <div class="chip l3">
        <div class="cl">L3 index (PTE)</div>
        <div class="cv" id="r-l3">—</div>
        <div class="cs">bits [29:21]</div>
      </div>
      <div class="chip off">
        <div class="cl">Page offset</div>
        <div class="cv" id="r-off">—</div>
        <div class="cs">bits [20:0]</div>
      </div>
      <div class="chip phys">
        <div class="cl">Physical address</div>
        <div class="cv" id="r-phys">—</div>
        <div class="cs">frame_base ‖ offset</div>
      </div>
    </div>
  </div>

  <p style="font-size:11px;color:var(--hint);text-align:center;padding-bottom:16px">
    Simulated — physical frame addresses are illustrative, not real memory. TLB is session-scoped.
  </p>
</div>

<script>
// ── Info text ──
const INFO = {
  res: '<strong>Reserved [63:48] — 16 bits.</strong> x86-64 uses only 48 bits. The top 16 must sign-extend bit 47 (canonical address). A non-canonical address causes a #GP (General Protection) fault immediately — no page walk happens.',
  l1:  '<strong>L1 index [47:39] — 9 bits → 512 entries.</strong> The CPU reads the CR3 register to find the PGD (Page Global Directory) base. It multiplies this 9-bit field × 8 bytes/entry and adds the result to the PGD base to read the PMD base address.',
  l2:  '<strong>L2 index [38:30] — 9 bits → 512 entries.</strong> The L1 entry gives the physical base of the PMD (Page Middle Directory). The CPU indexes it with bits [38:30] × 8 bytes to get the PTE table pointer.',
  l3:  '<strong>L3 index [29:21] — 9 bits → 512 entries.</strong> The L2 entry gives the physical base of the PTE table (Page Table Entry). Indexing it produces the final entry: physical frame number + R/W, U/S, NX, dirty, accessed bits.',
  off: '<strong>Page offset [20:0] — 21 bits → 2 MB pages.</strong> This field bypasses translation entirely — it addresses bytes within the physical frame. 2²¹ = 2,097,152 bytes per page. For 4 KB pages you use only 12 offset bits and need a 4th paging level.',
};

const PRESETS = {
  user:   140737488355328n,
  kernel: 18446744069414584320n,
};

const TLB = {};
let animTimer = null;

function segClick(seg) {
  document.querySelectorAll('.aseg').forEach(el => el.classList.remove('hl'));
  const el = document.querySelector('.aseg.' + seg);
  if (el) el.classList.add('hl');
  document.getElementById('infobox').innerHTML = INFO[seg] || '';
}

function getBits(va, hi, lo) {
  const mask = (1n << BigInt(hi - lo + 1)) - 1n;
  return Number((va >> BigInt(lo)) & mask);
}

function toHex(n, digits) {
  return '0x' + n.toString(16).toUpperCase().padStart(digits, '0');
}

function vaToHex64(va) {
  const lo = Number(va & 0xFFFFFFFFn);
  const hi = Number((va >> 32n) & 0xFFFFFFFFn);
  return '0x' + hi.toString(16).padStart(8, '0').toUpperCase()
              + lo.toString(16).padStart(8, '0').toUpperCase();
}

function updateHex() {
  try {
    const va = BigInt(document.getElementById('va-in').value) & 0xFFFFFFFFFFFFFFFFn;
    document.getElementById('hex-out').textContent = vaToHex64(va);
  } catch(e) {}
}

document.getElementById('va-in').addEventListener('input', updateHex);

document.getElementById('speed').addEventListener('input', function() {
  const v = +this.value;
  const labels = { 200:'Fast', 400:'Fast', 600:'Fast', 750:'Medium', 800:'Medium', 1000:'Slow', 1200:'Slow', 1500:'Slowest' };
  document.getElementById('speed-label').textContent = v <= 400 ? 'Fast' : v <= 850 ? 'Medium' : 'Slow';
});

function randomAddr() {
  const hi = BigInt(Math.floor(Math.random() * 0x8000));
  const lo = BigInt(Math.floor(Math.random() * 0xFFFFFFFF));
  const va = hi * 0x100000000n + lo;
  document.getElementById('va-in').value = String(va);
  updateHex();
}

function presetAddr(key) {
  document.getElementById('va-in').value = String(PRESETS[key]);
  updateHex();
}

function clearAll() {
  clearTimeout(animTimer);
  document.getElementById('anim-layer').innerHTML = '';
  document.getElementById('walk-status').textContent = 'Enter an address above and click Translate & Animate';
  document.getElementById('step-log').innerHTML = '<div style="color:var(--hint);font-style:italic">Walk steps will appear here after translation…</div>';
  document.getElementById('tlb-badge').style.display = 'none';
  document.getElementById('tlb-msg').textContent = '—';
  ['r-l1','r-l2','r-l3','r-off','r-phys'].forEach(id => document.getElementById(id).textContent = '—');
  ['t-l1e','t-l2e','t-l3e'].forEach(id => document.getElementById(id).textContent = 'entry [?]');
  document.getElementById('t-off').textContent = '21 bits direct';
  document.getElementById('t-phys').textContent = 'frame_base + offset';
  document.getElementById('t-tlb').textContent = 'Translation cache';
  document.getElementById('t-tlb2').textContent = '—';
}

function appendLog(cls, text) {
  const log = document.getElementById('step-log');
  if (log.querySelector('div[style*="italic"]')) log.innerHTML = '';
  const div = document.createElement('div');
  div.className = 'log-entry';
  div.innerHTML = `<span class="log-step log-${cls}">▶</span><span class="log-${cls}">${text}</span>`;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

function makeSvgEl(tag, attrs) {
  const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  return el;
}

function flashRect(id, color) {
  const el = document.getElementById(id);
  if (!el) return;
  const orig = el.getAttribute('fill');
  el.setAttribute('fill', color);
  setTimeout(() => el.setAttribute('fill', orig), 500);
}

function addFlowLine(layer, x1, y1, x2, y2, color, isDash) {
  const line = makeSvgEl('line', {
    x1, y1, x2, y2,
    stroke: color, 'stroke-width': '2.5',
    'stroke-linecap': 'round',
    'marker-end': 'url(#arr)',
    class: 'flow-line fade-in',
  });
  if (!isDash) line.style.strokeDasharray = '6 4';
  layer.appendChild(line);
}

function addFlowPath(layer, d, color) {
  const path = makeSvgEl('path', {
    d, fill: 'none',
    stroke: color, 'stroke-width': '2.5',
    'stroke-linecap': 'round',
    'marker-end': 'url(#arr)',
    class: 'flow-line fade-in',
  });
  layer.appendChild(path);
}

function addDot(layer, cx, cy, color) {
  const c = makeSvgEl('circle', { cx, cy, r: '5', fill: color, class: 'fade-in' });
  const ring = makeSvgEl('circle', { cx, cy, r: '5', fill: 'none', stroke: color, 'stroke-width': '2', class: 'pulse-ring fade-in' });
  layer.appendChild(c);
  layer.appendChild(ring);
}

function runTranslate() {
  clearTimeout(animTimer);
  document.getElementById('anim-layer').innerHTML = '';
  document.getElementById('step-log').innerHTML = '';

  let va;
  try { va = BigInt(document.getElementById('va-in').value) & 0xFFFFFFFFFFFFFFFFn; }
  catch(e) { alert('Invalid address'); return; }

  const l1  = getBits(va, 47, 39);
  const l2  = getBits(va, 38, 30);
  const l3  = getBits(va, 29, 21);
  const off = getBits(va, 20, 0);
  const frameBase = ((l1 * 512 + l2) * 512 + l3) * 0x200000;
  const physAddr  = frameBase + off;

  const speed = +document.getElementById('speed').value;

  // Update chips
  document.getElementById('r-l1').textContent  = l1  + ' (' + toHex(l1, 3)  + ')';
  document.getElementById('r-l2').textContent  = l2  + ' (' + toHex(l2, 3)  + ')';
  document.getElementById('r-l3').textContent  = l3  + ' (' + toHex(l3, 3)  + ')';
  document.getElementById('r-off').textContent = off + ' (' + toHex(off, 6) + ')';
  document.getElementById('r-phys').textContent = toHex(physAddr, 10);

  document.getElementById('t-l1e').textContent = 'entry[' + l1 + '] → PMD base';
  document.getElementById('t-l2e').textContent = 'entry[' + l2 + '] → PTE base';
  document.getElementById('t-l3e').textContent = 'entry[' + l3 + '] → frame';
  document.getElementById('t-off').textContent  = off + ' bytes (' + toHex(off, 6) + ')';
  document.getElementById('t-phys').textContent = toHex(physAddr, 10);
  document.getElementById('cr3-val').textContent = 'base=0x1000';
  updateHex();

  // TLB
  const key = l1 + '.' + l2 + '.' + l3;
  const tlbHit = !!TLB[key];
  TLB[key] = true;

  const badge = document.getElementById('tlb-badge');
  badge.style.display = 'inline-block';
  if (tlbHit) {
    badge.className = 'tlb-badge tlb-hit';
    badge.textContent = 'HIT';
    document.getElementById('tlb-msg').textContent = 'Frame cached — hardware skips the page walk.';
    document.getElementById('t-tlb').textContent = 'HIT — cached!';
    document.getElementById('t-tlb2').textContent = toHex(frameBase, 10);
  } else {
    badge.className = 'tlb-badge tlb-miss';
    badge.textContent = 'MISS';
    document.getElementById('tlb-msg').textContent = 'Not cached — 3 memory reads required for the walk.';
    document.getElementById('t-tlb').textContent = 'MISS — walking';
    document.getElementById('t-tlb2').textContent = 'tables…';
  }

  const layer = document.getElementById('anim-layer');
  const status = document.getElementById('walk-status');

  const STEPS = [
    {
      fn() {
        addFlowLine(layer, 112, 56, 178, 56, 'var(--p600)');
        addDot(layer, 178, 56, 'var(--p600)');
        flashRect('b-l1e', 'var(--p200)');
      },
      log: ['l1', 'CR3 → PGD base = 0x1000. Index with L1=' + l1 + ' → read entry[' + l1 + '] at offset +' + (l1*8) + ' B'],
      status: 'Step 1 — Reading L1 PGD at CR3 base, index ' + l1,
    },
    {
      fn() {
        addFlowLine(layer, 322, 56, 378, 56, 'var(--t600)');
        addDot(layer, 378, 56, 'var(--t600)');
        flashRect('b-l2e', 'var(--t200)');
      },
      log: ['l2', 'L1 entry[' + l1 + '] gives PMD base. Index with L2=' + l2 + ' → read entry[' + l2 + '] at offset +' + (l2*8) + ' B'],
      status: 'Step 2 — Reading L2 PMD, index ' + l2,
    },
    {
      fn() {
        addFlowLine(layer, 522, 56, 578, 56, 'var(--a600)');
        addDot(layer, 578, 56, 'var(--a600)');
        flashRect('b-l3e', 'var(--a200)');
      },
      log: ['l3', 'L2 entry[' + l2 + '] gives PTE base. Index with L3=' + l3 + ' → frame number in entry[' + l3 + ']'],
      status: 'Step 3 — Reading L3 PTE, index ' + l3,
    },
    {
      fn() {
        addFlowPath(layer, 'M650 100 L650 175 L600 228', 'var(--c600)');
        addDot(layer, 600, 228, 'var(--c600)');
        flashRect('b-phys', 'var(--c100)');
      },
      log: ['off', 'L3 entry[' + l3 + '] → frame base. Physical = frame_base + offset ' + off + ' = ' + toHex(physAddr, 10)],
      status: 'Step 4 — Adding page offset ' + off + ' to frame base',
    },
    {
      fn() {
        addFlowLine(layer, 250, 230, 498, 262, 'var(--c600)');
        addDot(layer, 498, 262, 'var(--c400)');
      },
      log: ['ok', '✓ Translation complete → physical address = ' + toHex(physAddr, 10)],
      status: 'Done — physical address = ' + toHex(physAddr, 10),
    },
  ];

  let i = 0;
  function doStep() {
    if (i >= STEPS.length) return;
    const s = STEPS[i++];
    s.fn();
    appendLog(s.log[0], s.log[1]);
    status.textContent = s.status;
    animTimer = setTimeout(doStep, speed);
  }

  status.textContent = 'Starting walk…';
  animTimer = setTimeout(doStep, 300);
}

updateHex();
</script>
</body>
</html>

    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)