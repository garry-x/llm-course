/* ================================================================
   LLM 深度学习课程 — 共享应用逻辑
   ================================================================ */
(function(){
  'use strict';

  var CHAPTERS = [
    {id:1, file:'ch01.html', title:'环境搭建与分词', desc:'实现BPE Tokenizer', sections:10},
    {id:2, file:'ch02.html', title:'嵌入层与位置编码', desc:'TokenEmbedding + RoPE', sections:9},
    {id:3, file:'ch03.html', title:'单头自注意力', desc:'Scaled Dot-Product Attention', sections:10},
    {id:4, file:'ch04.html', title:'多头注意力与MLA', desc:'MHA→GQA→DeepSeek MLA', sections:9},
    {id:5, file:'ch05.html', title:'Transformer Block', desc:'RMSNorm+FFN+SwiGLU+mHC', sections:10},
    {id:6, file:'ch06.html', title:'组装完整GPT模型', desc:'GPT-2 124M + DeepSeekMoE', sections:10},
    {id:7, file:'ch07.html', title:'训练循环', desc:'AdamW/Muon+FP8/FP4+DualPipe', sections:14},
    {id:8, file:'ch08.html', title:'文本生成', desc:'采样策略+MTP推测解码', sections:11},
    {id:9, file:'ch09.html', title:'微调与对齐', desc:'SFT/LoRA/DPO/GRPO', sections:12},
    {id:10, file:'ch10.html', title:'推理优化与前沿', desc:'KV Cache/CSA+HCA/量化/RAG', sections:14}
  ];

  // ---- State helpers ----
  function safeGet(k, fallback){
    try{ var v=localStorage.getItem(k); return v!==null?JSON.parse(v):fallback }
    catch(e){ return fallback }
  }
  function safeSet(k, v){ try{ localStorage.setItem(k, JSON.stringify(v)) } catch(e){} }

  var completed = new Set(safeGet('llm-done', []));
  var currentCh = parseInt(document.body.getAttribute('data-ch')||'0');

  // ---- Sidebar rendering ----
  function renderSidebar(){
    var nav = document.getElementById('sidebar-nav');
    if(!nav) return;
    var html = '';
    CHAPTERS.forEach(function(ch){
      var cls = (ch.id===currentCh?'active ':'')+(completed.has(ch.id)?'completed ':'');
      html += '<a href="'+ch.file+'" class="'+cls.trim()+'"'+
        (ch.id===currentCh?' aria-current="page"':'')+'>'+
        '<span class="ch-num">'+ch.id+'</span> '+ch.title+'</a>';
    });
    nav.innerHTML = html;
  }

  function updateProgress(){
    var bar = document.getElementById('progress-bar');
    var txt = document.getElementById('progress-text');
    if(!bar||!txt) return;
    var pct = Math.round(completed.size/CHAPTERS.length*100);
    bar.style.width = pct+'%';
    txt.textContent = completed.size+' / '+CHAPTERS.length;
  }

  // ---- Mark chapter complete (toggle) ----
  function markComplete(){
    if(completed.has(currentCh)) completed.delete(currentCh);
    else completed.add(currentCh);
    safeSet('llm-done', [...completed]);
    updateProgress();
    renderSidebar();
    var btn = document.getElementById('mark-complete');
    if(btn) btn.textContent = completed.has(currentCh) ? '✅ 已完成 (点击取消)' : '✓ 标记完成';
  }

  // ---- Theme ----
  function getTheme(){ return safeGet('llm-theme', 'light') }
  function toggleTheme(){
    var html = document.documentElement;
    var isDark = html.getAttribute('data-theme')==='dark';
    var next = isDark?'light':'dark';
    html.setAttribute('data-theme', next);
    safeSet('llm-theme', next);
    var icon = document.getElementById('theme-icon');
    var label = document.getElementById('theme-label');
    if(icon) icon.textContent = next==='dark'?'☀️':'🌙';
    if(label) label.textContent = next==='dark'?'浅色模式':'暗色模式';
  }
  function initTheme(){
    var t = getTheme();
    document.documentElement.setAttribute('data-theme', t);
    if(t==='dark'){
      var icon = document.getElementById('theme-icon');
      var label = document.getElementById('theme-label');
      if(icon) icon.textContent='☀️';
      if(label) label.textContent='浅色模式';
    }
  }

  // ---- Font size (small/medium/large) ----
  function setFontSize(size){
    document.documentElement.setAttribute('data-font', size);
    safeSet('llm-font', size);
    updateFontBtns(size);
  }
  function updateFontBtns(active){
    document.querySelectorAll('.font-btn').forEach(function(b){
      b.classList.toggle('active', b.getAttribute('data-size')===active);
    });
  }
  function initFontSize(){
    var saved = safeGet('llm-font', 'medium');
    document.documentElement.setAttribute('data-font', saved);
    updateFontBtns(saved);
  }

  // ---- Exercise check (MC) ----
  function checkMC(btn, groupName){
    var exEl = btn.closest('.exercise');
    var fb = exEl.querySelector('.feedback');
    var correctAns = exEl.getAttribute('data-answer');
    var explain = exEl.getAttribute('data-explain')||'';
    var selected = exEl.querySelector('input[name="'+groupName+'"]:checked');
    if(!selected){ fb.className='feedback show wrong'; fb.innerHTML='请先选择一个选项'; return; }
    if(selected.value===correctAns){
      fb.className='feedback show correct';
      fb.innerHTML='✅ 正确！ '+explain;
    } else {
      fb.className='feedback show wrong';
      fb.innerHTML='❌ 不正确。 '+explain;
    }
  }

  function showHint(btn){
    var exEl = btn.closest('.exercise');
    var fb = exEl.querySelector('.feedback');
    fb.className='feedback show hint';
    fb.innerHTML='💡 <strong>提示：</strong>'+exEl.getAttribute('data-explain');
  }

  // ---- Back to top ----
  function initBackToTop(){
    var btn = document.getElementById('back-to-top');
    if(!btn) return;
    window.addEventListener('scroll', function(){
      btn.classList.toggle('visible', window.scrollY > 400);
    });
  }

  // ---- Keyboard nav ----
  function initKeyboardNav(){
    document.addEventListener('keydown', function(e){
      var tag = e.target.tagName;
      if(tag==='INPUT'||tag==='TEXTAREA'||tag==='SELECT'||e.target.isContentEditable) return;
      if(e.key==='Escape'){ document.getElementById('sidebar').classList.remove('open'); return; }
      if(e.key==='ArrowLeft'){
        e.preventDefault();
        var prev = document.querySelector('.chapter-nav a[rel="prev"]');
        if(prev) location.href = prev.href;
      } else if(e.key==='ArrowRight'){
        e.preventDefault();
        var next = document.querySelector('.chapter-nav a[rel="next"]');
        if(next) location.href = next.href;
      }
    });
  }

  // ---- Mobile sidebar ----
  function initSidebarToggle(){
    var toggle = document.querySelector('.menu-toggle');
    var sidebar = document.getElementById('sidebar');
    if(!toggle||!sidebar) return;
    toggle.addEventListener('click', function(){ sidebar.classList.toggle('open') });
  }

  // ---- Init ----
  function init(){
    initTheme();
    initFontSize();
    renderSidebar();
    updateProgress();
    initBackToTop();
    initKeyboardNav();
    initSidebarToggle();
    // KaTeX
    if(window.renderMathInElement){
      renderMathInElement(document.body, { delimiters: [
        {left:'\\[',right:'\\]',display:true},
        {left:'\\(',right:'\\)',display:false}
      ], throwOnError: false });
    }
    if(window.katex){
      document.querySelectorAll('.katex-inline').forEach(function(el){
        try{ katex.render(el.getAttribute('data-expr'), el, {throwOnError:false}) }
        catch(e){ el.textContent='[公式错误]' }
      });
      document.querySelectorAll('.katex:not(.katex-inline)').forEach(function(el){
        var expr = el.getAttribute('data-expr');
        if(!expr) return;
        try{ katex.render(expr, el, {displayMode:true, throwOnError:false}) }
        catch(e){ el.textContent='[公式错误]' }
      });
    }
  }

  // Public API
  window.LLM = {
    checkMC: checkMC,
    showHint: showHint,
    toggleTheme: toggleTheme,
    markComplete: markComplete,
    setFontSize: setFontSize
  };

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
