/* ================================================================
   LLM 深度学习课程 — 共享应用逻辑
   ================================================================ */
(function(){
  'use strict';

  var CHAPTERS = [
    {id:1, file:'ch01.html', title:'环境搭建与分词', desc:'实现BPE Tokenizer', sections:10},
    {id:2, file:'ch02.html', title:'嵌入层与位置编码', desc:'TokenEmbedding + RoPE + PromptEng', sections:11},
    {id:3, file:'ch03.html', title:'单头自注意力', desc:'Scaled Dot-Product Attention', sections:10},
    {id:4, file:'ch04.html', title:'多头注意力与MLA', desc:'MHA→GQA→DeepSeek MLA', sections:9},
    {id:5, file:'ch05.html', title:'Transformer Block', desc:'RMSNorm+FFN+SwiGLU+mHC', sections:10},
    {id:6, file:'ch06.html', title:'组装完整GPT模型', desc:'GPT-2 124M + DeepSeekMoE', sections:10},
    {id:7, file:'ch07.html', title:'训练循环', desc:'AdamW/Muon+FP8/FP4+DualPipe+分布式', sections:15},
    {id:8, file:'ch08.html', title:'文本生成', desc:'采样策略+MTP推测解码+约束生成', sections:12},
    {id:9, file:'ch09.html', title:'微调与对齐', desc:'SFT/LoRA/DPO/GRPO', sections:12},
    {id:10, file:'ch10.html', title:'推理优化与前沿', desc:'KV Cache/CSA+HCA/量化/RAG/vLLM/Triton', sections:19}
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
    if(btn){
      btn.textContent = completed.has(currentCh) ? '✅ 已完成 (点击取消)' : '✓ 标记完成';
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
    var toc = document.createElement('div');
    toc.className = 'toc';
    toc.innerHTML = '<h4>📑 本章目录</h4><ol>' +
      Array.from(sections).map(function(s){
        var h3 = s.querySelector('h3');
        var title = h3 ? h3.textContent : s.id;
        return '<li><a href="#'+s.id+'">'+title+'</a></li>';
      }).join('') + '</ol>';
    var subtitle = chapter.querySelector('.reading-time');
    if(subtitle) subtitle.after(toc);
    // Highlight on scroll (throttled via rAF)
    var tocLinks = toc.querySelectorAll('a');
    var _tocRaf = false;
    window.addEventListener('scroll', function(){
      if(_tocRaf) return;
      _tocRaf = true;
      requestAnimationFrame(function(){
        _tocRaf = false;
        var scrollY = window.scrollY + 120;
        sections.forEach(function(s, i){
          if(s.offsetTop <= scrollY && (!sections[i+1] || sections[i+1].offsetTop > scrollY)){
            tocLinks.forEach(function(a){ a.classList.remove('toc-active') });
            if(tocLinks[i]) tocLinks[i].classList.add('toc-active');
          }
        });
      });
    }, {passive: true});
    // Smooth scroll
    tocLinks.forEach(function(a){
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
      btn.title = '复制代码';
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

  // ---- Search ----
  var searchIdx = [];
  function buildSearchIdx(){
    CHAPTERS.forEach(function(ch){
      searchIdx.push({id:ch.id, file:ch.file, title:ch.title, desc:ch.desc});
    });
  }
  function handleSearch(val){
    var box = document.getElementById('search-results');
    if(!box) return;
    if(!val || val.length < 2){ box.style.display='none'; box.innerHTML=''; return; }
    var q = val.toLowerCase();
    var matches = searchIdx.filter(function(item){
      return item.title.toLowerCase().indexOf(q)>=0 || item.desc.toLowerCase().indexOf(q)>=0;
    });
    if(matches.length===0){
      box.style.display='block';
      box.innerHTML = '<div style="padding:6px 8px;opacity:.5;font-size:.72rem">未找到匹配章节</div>';
    } else {
      box.style.display='block';
      box.innerHTML = matches.map(function(m){
        return '<a href="'+m.file+'" style="display:block;padding:6px 8px;color:var(--sidebar-text);text-decoration:none;border-radius:4px;font-size:.72rem"'+
          ' onmouseover="this.style.background=\'rgba(255,255,255,.08)\'" onmouseout="this.style.background=\'transparent\'">'+
          '<span style="color:var(--accent);font-weight:600">Ch'+m.id+'</span> '+m.title+'</a>';
      }).join('');
    }
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
    initTOC();
    initCodeCopy();
    initReadingBar();
    buildSearchIdx();
    // Bind search
    var searchBox = document.getElementById('search-box');
    if(searchBox) searchBox.addEventListener('input', function(){ handleSearch(this.value); });
    // KaTeX
    if(window.katex){
      var macros = { '\\parallel': '\\mathrel{/\\!\\!/}' };
      document.querySelectorAll('.katex-inline').forEach(function(el){
        try{ katex.render(el.getAttribute('data-expr'), el, {throwOnError:true, strict:false, macros:macros, trust:true}) }
        catch(e){ console.warn('KaTeX inline:', el.getAttribute('data-expr'), e.message); el.textContent=el.getAttribute('data-expr'); el.style.color='#cc4444'; }
      });
      document.querySelectorAll('.katex:not(.katex-inline)').forEach(function(el){
        var expr = el.getAttribute('data-expr');
        if(!expr) return;
        try{ katex.render(expr, el, {displayMode:true, throwOnError:true, strict:false, macros:macros, trust:true}) }
        catch(e){ console.warn('KaTeX display:', expr, e.message); el.textContent=expr; el.style.color='#cc4444'; }
      });
    }
  }

  // Public API
  window.LLM = {
    checkMC: checkMC,
    showHint: showHint,
    toggleTheme: toggleTheme,
    markComplete: markComplete,
    setFontSize: setFontSize,
    toggleSolution: function(btn){ btn.classList.toggle('open'); btn.nextElementSibling.classList.toggle('open'); }
  };

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
