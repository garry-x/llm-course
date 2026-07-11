/* ================================================================
   LLM Deep Learning Course — Shared Application Logic
   ================================================================ */
(function(){
  'use strict';

  var CHAPTERS = [
    {id:1, file:'ch01.html', title:'Environment Setup & Tokenization', navTitle:'Tokenization', desc:'BPE, multilingual tokenizer, special tokens & model interface contract', zhTitle:'环境搭建与分词', zhNavTitle:'分词与 BPE', zhDesc:'BPE、多语言 tokenizer、special tokens 与模型接口契约', sections:19},
    {id:2, file:'ch02.html', title:'Embedding Layer & Positional Encoding', navTitle:'Embeddings & RoPE', desc:'TokenEmbedding, word vectors, contextualized representations, RoPE, long context & prompt representation', zhTitle:'Embedding 层与位置编码', zhNavTitle:'Embedding 与 RoPE', zhDesc:'TokenEmbedding、词向量、上下文化表示、RoPE、长上下文与 prompt 表示', sections:20},
    {id:3, file:'ch03.html', title:'Single-Head Self-Attention', navTitle:'Self-Attention', desc:'Scaled Dot-Product Attention, mask, masked softmax, diagnostic ledger & complexity bounds', zhTitle:'单头自注意力', zhNavTitle:'自注意力', zhDesc:'Scaled Dot-Product Attention、mask、masked softmax、诊断台账与复杂度边界', sections:20},
    {id:4, file:'ch04.html', title:'Multi-Head Attention & MLA', navTitle:'Multi-Head & MLA', desc:'MHA, GQA, MLA, KV Cache budget & checkpoint conversion', zhTitle:'多头注意力与 MLA', zhNavTitle:'多头注意力与 MLA', zhDesc:'MHA、GQA、MLA、KV Cache 预算与 checkpoint 转换', sections:18},
    {id:5, file:'ch05.html', title:'Transformer Block', navTitle:'Transformer Block', desc:'RMSNorm, SwiGLU, resource estimation, stability & interpretability', zhTitle:'Transformer Block', zhNavTitle:'Transformer Block', zhDesc:'RMSNorm、SwiGLU、资源估算、稳定性与可解释性', sections:20},
    {id:6, file:'ch06.html', title:'Assembling a Complete GPT Model', navTitle:'GPT Model', desc:'GPT-2 124M, MoE, weight loading, logit parity & checkpoint compatibility', zhTitle:'组装完整 GPT 模型', zhNavTitle:'GPT 模型', zhDesc:'GPT-2 124M、MoE、权重加载、logit parity 与 checkpoint 兼容性', sections:18},
    {id:7, file:'ch07.html', title:'Training Loop', navTitle:'Training', desc:'Data pipeline, AdamW, checkpoint, distributed, MFU, industrial training diagnostics', zhTitle:'训练循环', zhNavTitle:'训练循环', zhDesc:'数据流水线、AdamW、checkpoint、分布式、MFU 与工业训练诊断', sections:26},
    {id:8, file:'ch08.html', title:'Text Generation', navTitle:'Generation', desc:'Sampling, beam, thinking budget, speculative & structured decoding', zhTitle:'文本生成', zhNavTitle:'文本生成', zhDesc:'采样、beam、thinking budget、speculative decoding 与结构化输出', sections:25},
    {id:9, file:'ch09.html', title:'Fine-Tuning & Alignment', navTitle:'Alignment', desc:'SFT, synthetic distillation, LoRA, DPO, GRPO, rollout systems & retention', zhTitle:'微调与对齐', zhNavTitle:'微调与对齐', zhDesc:'SFT、synthetic distillation、LoRA、DPO、GRPO、rollout 系统与能力保持', sections:27},
    {id:10, file:'ch10.html', title:'Inference Optimization & Frontiers', navTitle:'Inference', desc:'KV Cache, sparse/linear attention, continuous batching, RAG & KV-aware orchestration', zhTitle:'推理优化与前沿', zhNavTitle:'推理优化', zhDesc:'KV Cache、稀疏/线性注意力、continuous batching、RAG 与 KV-aware orchestration', sections:38},
    {id:11, file:'ch11.html', title:'Classical Neural NLP & Evaluation', navTitle:'NLP & Evaluation', desc:'RNN, Parsing, Seq2Seq, BERT, capstone evidence & safety', zhTitle:'经典神经 NLP 与评估', zhNavTitle:'NLP 与评估', zhDesc:'RNN、Parsing、Seq2Seq、BERT、结课项目证据与 safety', sections:21}
  ];

  // ---- State helpers (localStorage-backed) ----
  function safeGet(k, fb){
    try{
      var v = localStorage.getItem(k);
      if(v === null){
        v = localStorage.getItem('__idb_' + k);
        if(v !== null) localStorage.setItem(k, v);
      }
      return v ? JSON.parse(v) : fb;
    } catch(e){ return fb }
  }
  function safeSet(k, v){
    try{
      localStorage.setItem(k, JSON.stringify(v));
      localStorage.removeItem('__idb_' + k);
    } catch(e){}
  }

  var completed = new Set(safeGet('llm-done', []));
  var currentCh = parseInt(document.body.getAttribute('data-ch')||'0');

  function isEnglishPage(){
    return (document.documentElement.getAttribute('lang') || '').toLowerCase().indexOf('en') === 0;
  }

  function homeHref(){
    var explicitHome = document.body.getAttribute('data-home-href');
    if(explicitHome) return explicitHome;
    if(isEnglishPage()) return currentCh === 0 ? 'en.html' : '../en.html';
    return currentCh === 0 ? 'index.html' : '../../index.html';
  }

  function chapterHref(ch){
    var explicitPrefix = document.body.getAttribute('data-chapter-prefix');
    if(currentCh === 0) return (explicitPrefix || 'chapters/') + ch.file;
    return ch.file;
  }

  function languageHref(){
    var explicitLanguage = document.body.getAttribute('data-language-href');
    if(explicitLanguage) return explicitLanguage;
    if(isEnglishPage()){
      return currentCh === 0 ? 'index.html' : '../zh/chapters/' + CHAPTERS[currentCh - 1].file;
    }
    return currentCh === 0 ? '../en.html' : '../../chapters/' + CHAPTERS[currentCh - 1].file;
  }

  function chaptersWithHref(){
    var zh = !isEnglishPage();
    return CHAPTERS.map(function(ch){
      return {
        id: ch.id,
        file: chapterHref(ch),
        title: zh ? ch.zhTitle : ch.title,
        desc: zh ? ch.zhDesc : ch.desc,
        sections: ch.sections
      };
    });
  }

  // ---- Sidebar rendering ----
  function renderLanguageSwitch(){
    var header = document.querySelector('.sidebar-header');
    if(!header) return;
    var existing = header.querySelector('.language-switch');
    if(existing) existing.remove();
    var zh = !isEnglishPage();
    var currentHref = homeHref();
    var otherHref = languageHref();
    var html = '<div class="language-switch" aria-label="Language">';
    html += zh
      ? '<span class="active" aria-current="true">中文</span><a href="'+otherHref+'">EN</a>'
      : '<a href="'+otherHref+'">中文</a><span class="active" aria-current="true">EN</span>';
    html += '</div>';
    header.insertAdjacentHTML('beforeend', html);
  }

  function renderSidebar(){
    var nav = document.getElementById('sidebar-nav');
    if(!nav) return;
    var zh = !isEnglishPage();
    var html = '<a href="'+homeHref()+'" class="'+(currentCh===0?'active ':'')+'home-link"'+
      (currentCh===0?' aria-current="page"':'')+'>'+
      '<span class="ch-num">⌂</span><span class="ch-label">'+(zh?'中文首页':'Home')+'</span></a>';
    CHAPTERS.forEach(function(ch){
      var cls = (ch.id===currentCh?'active ':'')+(completed.has(ch.id)?'completed ':'');
      html += '<a href="'+chapterHref(ch)+'" class="'+cls.trim()+'" title="'+(zh?ch.zhTitle:ch.title)+'"'+
        (ch.id===currentCh?' aria-current="page"':'')+'>'+
        '<span class="ch-num">'+ch.id+'</span><span class="ch-label">'+(zh?ch.zhNavTitle:ch.navTitle)+'</span></a>';
    });
    nav.innerHTML = html;
  }

  function initHomeLinks(){
    document.querySelectorAll('.sidebar-header h1').forEach(function(title){
      if(title.querySelector('a')) return;
      title.innerHTML = '<a href="'+homeHref()+'">'+title.textContent+'</a>';
    });
  }

  function updateCompleteButton(){
    var btn = document.getElementById('mark-complete');
    if(btn) btn.textContent = completed.has(currentCh)
      ? (isEnglishPage() ? '✅ Completed (Click to undo)' : '✅ 已完成（点击撤销）')
      : (isEnglishPage() ? '✓ Mark Complete' : '✓ 标记完成');
  }

  function renderHomeChapterList(){
    if(document.body.getAttribute('data-page') !== 'home') return;
    var list = document.getElementById('chapter-list');
    if(!list) return;
    var done = new Set(safeGet('llm-done',[]));
    list.innerHTML = chaptersWithHref().map(function(ch){
      var isDone = done.has(ch.id);
      return '<a href="'+ch.file+'" class="chapter-item'+(isDone?' completed':'')+'">'+
        '<span class="ch-num-big">'+(isDone?'✓':ch.id)+'</span>'+
        '<span class="ch-info"><h4>'+(isEnglishPage()?'Chapter ':'第 ')+ch.id+(isEnglishPage()?' ':' 章 ')+ch.title+'</h4><p>'+ch.desc+'</p></span>'+
        '<span class="ch-meta">'+ch.sections+(isEnglishPage()?' sections':' 小节')+'</span></a>';
    }).join('');
  }

  // ---- Mark chapter complete (toggle) ----
  function markComplete(){
    if(completed.has(currentCh)) completed.delete(currentCh);
    else completed.add(currentCh);
    safeSet('llm-done', [...completed]);
    renderSidebar();
    updateCompleteButton();
    var btn = document.getElementById('mark-complete');
    if(btn){
      if(completed.has(currentCh)){
        btn.classList.add('celebrate');
        setTimeout(function(){ btn.classList.remove('celebrate'); }, 500);
      }
    }
  }

  // ---- Theme ----
  function getTheme(){ return safeGet('llm-theme', 'light') }
  function toggleTheme(){
    var html = document.documentElement;
    var isDark = html.getAttribute('data-theme')==='dark';
    var next = isDark?'light':'dark';
    html.setAttribute('data-theme', next);
    safeSet('llm-theme', next);
    updateThemeLabel(next);
  }
  function updateThemeLabel(theme){
    var icon = document.getElementById('theme-icon');
    var label = document.getElementById('theme-label');
    if(icon) icon.textContent = theme==='dark'?'☀️':'🌙';
    if(label) label.textContent = theme==='dark'
      ? (isEnglishPage()?'Light Mode':'浅色模式')
      : (isEnglishPage()?'Dark Mode':'深色模式');
  }
  function initTheme(){
    var t = getTheme();
    document.documentElement.setAttribute('data-theme', t);
    updateThemeLabel(t);
  }

  // ---- Font size ----
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
    if(!exEl) return;
    var fb = exEl.querySelector('.feedback');
    var correctAns = exEl.getAttribute('data-answer');
    var explain = exEl.getAttribute('data-explain')||'';
    var selected = exEl.querySelector('input[name="'+groupName+'"]:checked');
    if(!selected){ fb.className='feedback show wrong'; fb.innerHTML=isEnglishPage()?'Please select an option first':'请先选择一个选项'; return; }
    if(selected.value===correctAns){
      fb.className='feedback show correct';
      fb.innerHTML=(isEnglishPage()?'✅ Correct! ':'✅ 答对了。')+explain;
    } else {
      fb.className='feedback show wrong';
      fb.innerHTML=(isEnglishPage()?'❌ Incorrect. ':'❌ 不对。')+explain;
    }
  }

  function showHint(btn){
    var exEl = btn.closest('.exercise');
    var fb = exEl.querySelector('.feedback');
    fb.className='feedback show hint';
    fb.innerHTML=(isEnglishPage()?'💡 <strong>Hint:</strong>':'💡 <strong>提示：</strong>')+exEl.getAttribute('data-explain');
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

  // ---- Sidebar toggle (mobile + tablet tap) ----
  function initSidebarToggle(){
    var toggle = document.querySelector('.menu-toggle');
    var sidebar = document.getElementById('sidebar');
    if(!toggle||!sidebar) return;
    toggle.addEventListener('click', function(e){
      e.stopPropagation();
      sidebar.classList.toggle('open');
    });
    // Tablet: tap sidebar to expand when collapsed
    sidebar.addEventListener('click', function(e){
      if(window.innerWidth <= 959 && window.innerWidth > 639 && !sidebar.classList.contains('open')){
        sidebar.classList.add('expanded');
        setTimeout(function(){ sidebar.classList.remove('expanded'); }, 3000);
      }
    });
  }

  // ---- TOC Generation ----
  function initTOC(){
    var chapter = document.querySelector('.chapter');
    if(!chapter) return;
    var sections = chapter.querySelectorAll('section.card[id]');
    if(sections.length < 3) return;
    function escapeHTML(value){
      return String(value).replace(/[&<>"']/g, function(ch){
        return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch];
      });
    }
    function compactTocTitle(title){
      var compact = String(title).trim()
        .replace(/^\d+(?:\.\d+)*[A-Z]?\s+/, '')
        .replace(/^Programming Exercises?\s+([0-9-]+):\s*/i, 'Exercise $1: ')
        .replace(/^Chapter Summary:\s*/i, 'Summary: ');
      if(/^Exercise\s+[0-9-]+$/.test(compact)) return compact;
      compact = compact.split(/\s*[—–]\s*|\s+-\s+|:\s+/)[0];
      return compact
        .replace(/^BPE as Data-Driven Compression$/, 'BPE Compression')
        .replace(/^Detailed Analysis$/, 'Compression Heuristic')
        .replace(/^Encoding and Decoding$/, 'Encoding & Decoding')
        .replace(/^Comparison of Mainstream Tokenizers$/, 'Tokenizer Comparison')
        .replace(/^Tokenizer is the Model Interface Contract$/, 'Tokenizer Contract')
        .replace(/^Chat Template and Multimodal Interface Ledger$/, 'Chat & Multimodal Ledger')
        .replace(/^Multilingual Tokenizer Training$/, 'Multilingual Tokenizer');
    }
    var sectionItems = Array.from(sections).map(function(s){
      var h3 = s.querySelector('h3');
      var title = h3 ? h3.textContent : s.id;
      return {
        id: s.id,
        title: title,
        compactTitle: compactTocTitle(title)
      };
    });

    function renderTocItems(compact){
      return sectionItems.map(function(item){
        var safeTitle = escapeHTML(item.title);
        var label = escapeHTML(compact ? item.compactTitle : item.title);
        return '<li><a href="#'+item.id+'" title="'+safeTitle+'"><span class="toc-text">'+label+'</span></a></li>';
      }).join('');
    }

    function buildToc(className, title, compact){
      var toc = document.createElement('nav');
      toc.className = className;
      toc.setAttribute('aria-label', isEnglishPage() ? 'Chapter sections' : '章节目录');
      toc.innerHTML = '<h4>'+title+'</h4><ol>' + renderTocItems(compact) + '</ol>';
      return toc;
    }

    document.body.classList.add('has-page-toc');

    var inlineToc = buildToc('toc toc-inline', isEnglishPage() ? '📑 Table of Contents' : '📑 本章目录', false);
    var subtitle = chapter.querySelector('.reading-time');
    if(subtitle) subtitle.after(inlineToc);

    var sideToc = null;
    var main = document.querySelector('.main');
    if(currentCh >= 1 && main){
      sideToc = buildToc('chapter-page-toc', isEnglishPage() ? 'On This Page' : '本页内容', true);
      main.appendChild(sideToc);
    }

    // Highlight on scroll (throttled via rAF)
    function allTocLinks(){
      return document.querySelectorAll('.toc a,.chapter-page-toc a');
    }
    function updateTocActive(){
      var scrollY = window.scrollY + 120;
      var activeId = sections[0].id;
      sections.forEach(function(s){
        if(s.offsetTop <= scrollY) activeId = s.id;
      });
      allTocLinks().forEach(function(a){
        a.classList.toggle('toc-active', a.getAttribute('href') === '#'+activeId);
      });
    }
    var _tocRaf = false;
    window.addEventListener('scroll', function(){
      if(_tocRaf) return;
      _tocRaf = true;
      requestAnimationFrame(function(){
        _tocRaf = false;
        updateTocActive();
      });
    }, {passive: true});
    updateTocActive();
    // Smooth scroll
    allTocLinks().forEach(function(a){
      a.addEventListener('click', function(e){
        e.preventDefault();
        var target = document.querySelector(a.getAttribute('href'));
        if(target) window.scrollTo({top:target.offsetTop-30,behavior:'smooth'});
      });
    });
  }

  // ---- Code Copy (with HTTP fallback) ----
  function fallbackCopy(text, cb, btnRef){
    var ta = document.createElement('textarea');
    ta.value = text; ta.style.position='fixed'; ta.style.opacity='0';
    document.body.appendChild(ta); ta.select();
    try{ document.execCommand('copy'); if(cb) cb(); }
    catch(e){ if(btnRef){ btnRef.innerHTML = '⚠'; setTimeout(function(){ btnRef.innerHTML = '📋'; }, 1500); } }
    document.body.removeChild(ta);
  }

  function initCodeCopy(){
    document.querySelectorAll('.code-block').forEach(function(block){
      var wrap = document.createElement('div');
      wrap.className = 'code-block-wrap';
      block.parentNode.insertBefore(wrap, block);
      wrap.appendChild(block);
      var btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.title = 'Copy code';
      btn.innerHTML = '📋';
      btn.addEventListener('click', function(){
        var text = block.textContent;
        if(text.endsWith('\n')) text = text.slice(0,-1);
        var done = function(){
          btn.classList.add('copied');
          btn.innerHTML = '✓';
          setTimeout(function(){ btn.classList.remove('copied'); btn.innerHTML = '📋'; }, 2000);
        };
        if(navigator.clipboard && navigator.clipboard.writeText){
          navigator.clipboard.writeText(text).then(done).catch(function(){
            fallbackCopy(text, done, btn);
          });
        } else {
          fallbackCopy(text, done, btn);
        }
      });
      wrap.appendChild(btn);
    });
  }

  // ---- Reading Progress Bar (GPU-composited transform + rAF throttle) ----
  var _barRaf = false;
  function initReadingBar(){
    var bar = document.createElement('div');
    bar.className = 'reading-bar';
    bar.id = 'reading-bar';
    bar.style.transformOrigin = 'left';
    bar.style.transform = 'scaleX(0)';
    document.body.appendChild(bar);
    window.addEventListener('scroll', function(){
      if(_barRaf) return;
      _barRaf = true;
      requestAnimationFrame(function(){
        _barRaf = false;
        var scrollH = document.documentElement.scrollHeight - window.innerHeight;
        if(scrollH <= 0) return;
        bar.style.transform = 'scaleX(' + Math.min(1, window.scrollY / scrollH) + ')';
      });
    }, {passive: true});
  }

  // ---- Init ----
  function init(){
    initTheme();
    initFontSize();
    initHomeLinks();
    renderLanguageSwitch();
    renderSidebar();
    renderHomeChapterList();
    updateCompleteButton();
    initBackToTop();
    initKeyboardNav();
    initSidebarToggle();
    initTOC();
    initCodeCopy();
    initReadingBar();
    // KaTeX
    function renderMathFallback(){
      document.querySelectorAll('.katex-inline,.katex-block,.katex[data-expr]').forEach(function(el){
        var expr = el.getAttribute('data-expr');
        if(!expr) return;
        if(!el.getAttribute('aria-label')) el.setAttribute('aria-label', expr);
        if(!el.getAttribute('role')) el.setAttribute('role', 'img');
        if(!el.textContent) el.textContent = expr;
        el.classList.add('math-fallback');
      });
    }
    if(window.katex){
      var macros = { '\\parallel': '\\mathrel{/\\!\\!/}' };
      function prepareMathNode(el, expr){
        if(!expr) return;
        if(!el.getAttribute('aria-label')) el.setAttribute('aria-label', expr);
        if(!el.getAttribute('role')) el.setAttribute('role', 'img');
      }
      document.querySelectorAll('.katex-inline').forEach(function(el){
        var expr = el.getAttribute('data-expr');
        prepareMathNode(el, expr);
        try{ katex.render(expr, el, {throwOnError:true, strict:false, macros:macros, trust:true}) }
        catch(e){ console.warn('KaTeX inline:', expr, e.message); el.textContent=expr; el.style.color='#cc4444'; }
      });
      document.querySelectorAll('.katex:not(.katex-inline)').forEach(function(el){
        var expr = el.getAttribute('data-expr');
        if(!expr) return;
        prepareMathNode(el, expr);
        try{ katex.render(expr, el, {displayMode:true, throwOnError:true, strict:false, macros:macros, trust:true}) }
        catch(e){ console.warn('KaTeX display:', expr, e.message); el.textContent=expr; el.style.color='#cc4444'; }
      });
    } else {
      renderMathFallback();
    }
  }

  // Public API
  window.LLM = {
    checkMC: checkMC,
    showHint: showHint,
    toggleTheme: toggleTheme,
    markComplete: markComplete,
    setFontSize: setFontSize,
    toggleSolution: function(btn){ btn.classList.toggle('open'); btn.nextElementSibling.classList.toggle('open'); },
    getChapters: chaptersWithHref,
    renderHomeChapterList: renderHomeChapterList
  };

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
