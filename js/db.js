/* ================================================================
   LLM Learner — IndexedDB Local Database
   Dual-write strategy: localStorage cache (immediate read/write) + IndexedDB persistence (backup)
   On startup, restore localStorage from IndexedDB
   ================================================================ */
(function(){
  'use strict';

  var DB_NAME = 'llm-learner';
  var DB_VERSION = 1;
  var STORE = 'kv';
  var PREFIX = '__idb_'; // localStorage cache key prefix

  function openDB(){
    return new Promise(function(resolve, reject){
      var req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = function(e){
        if(!e.target.result.objectStoreNames.contains(STORE)){
          e.target.result.createObjectStore(STORE);
        }
      };
      req.onsuccess = function(e){ resolve(e.target.result) };
      req.onerror = function(){ reject(req.error) };
    });
  }

  function idbSet(db, key, val){
    return new Promise(function(resolve, reject){
      try{
        var tx = db.transaction(STORE, 'readwrite');
        tx.objectStore(STORE).put(val, key);
        tx.oncomplete = resolve;
        tx.onerror = function(){ reject(tx.error) };
      } catch(e){ reject(e) }
    });
  }

  function idbGetAll(db){
    return new Promise(function(resolve, reject){
      try{
        var tx = db.transaction(STORE, 'readonly');
        var req = tx.objectStore(STORE).getAll();
        var keysReq = tx.objectStore(STORE).getAllKeys();
        var results = {};
        req.onsuccess = function(){
          keysReq.onsuccess = function(){
            var keys = keysReq.result;
            var vals = req.result;
            for(var i=0; i<keys.length; i++){ results[keys[i]] = vals[i] }
            resolve(results);
          };
        };
        req.onerror = function(){ reject(req.error) };
      } catch(e){ reject(e) }
    });
  }

  // ---- Public API (sync, localStorage-backed, write-through to IDB) ----

  var _db = null;
  var _ready = false;

  // Bootstrap: load all IDB data into localStorage cache
  openDB().then(function(db){
    _db = db; _ready = true;
    return idbGetAll(db);
  }).then(function(all){
    // Restore all data from IndexedDB into localStorage cache
    Object.keys(all).forEach(function(k){
      try{
        localStorage.setItem(PREFIX + k, JSON.stringify(all[k]));
      } catch(e){}
    });
    // Also migrate old non-prefixed localStorage keys to IDB
    var oldKeys = ['llm-done','llm-theme','llm-font','llm-profiles','llm-active-profile'];
    oldKeys.forEach(function(k){
      var v = localStorage.getItem(k);
      if(v !== null && !localStorage.getItem(PREFIX + k)){
        localStorage.setItem(PREFIX + k, v);
        idbSet(_db, k, JSON.parse(v)).catch(function(){});
      }
    });
    // Migrate notes
    for(var i=0; i<localStorage.length; i++){
      var key = localStorage.key(i);
      if(key && key.indexOf('llm-notes-')===0 && !localStorage.getItem(PREFIX + key)){
        try{
          localStorage.setItem(PREFIX + key, localStorage.getItem(key));
          idbSet(_db, key, JSON.parse(localStorage.getItem(key))).catch(function(){});
        } catch(e){}
      }
    }
    console.log('[DB] IndexedDB ready, ' + Object.keys(all).length + ' keys loaded');
  }).catch(function(e){
    console.warn('[DB] IndexedDB unavailable, using localStorage only:', e.message);
  });

  // Sync get (from localStorage cache)
  function get(key, fallback){
    try{
      var v = localStorage.getItem(PREFIX + key);
      if(v !== null) return JSON.parse(v);
      // Fallback to old non-prefixed key
      var old = localStorage.getItem(key);
      if(old !== null){ set(key, JSON.parse(old)); return JSON.parse(old) }
    } catch(e){}
    return fallback;
  }

  // Sync set (localStorage + background IDB)
  function set(key, value){
    try{ localStorage.setItem(PREFIX + key, JSON.stringify(value)) } catch(e){}
    if(_db){
      idbSet(_db, key, value).catch(function(){});
    } else {
      // Queue for when DB is ready
      openDB().then(function(db){ _db = db; _ready = true; return idbSet(db, key, value) }).catch(function(){});
    }
  }

  // Sync remove
  function remove(key){
    try{ localStorage.removeItem(PREFIX + key) } catch(e){}
    if(_db){
      try{
        var tx = _db.transaction(STORE, 'readwrite');
        tx.objectStore(STORE).delete(key);
      } catch(e){}
    }
  }

  // Expose
  window.IDB = { get: get, set: set, remove: remove, ready: function(){ return _ready } };
})();