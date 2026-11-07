var v86_config={
 bios:{url:"./v86/bios/seabios.bin"},
 vga_bios:{url:"./v86/bios/vgabios.bin"},
 hda:{url:"./v86/images/200.img"},
 autostart:true,
 memory_size:128*1024*1024,
 wasm_path:"./v86/build/v86.wasm"
};
document.addEventListener("DOMContentLoaded",()=>{
  window.emulator=new V86Starter(v86_config);
  setTimeout(()=>{try{emulator.focus()}catch(e){}},1200);
});

window.sendBluh=function(){
  emulator.keyboard_send_text("cat > /bin/bluh <<'EOF'\n#!/bin/sh\necho \"bluh $@\"\nEOF\nchmod +x /bin/bluh\nclear\nbluh ready\n");
};
document.addEventListener("DOMContentLoaded",()=>{ setTimeout(()=>{try{sendBluh()}catch(e){}},25000); });

(function(){
  var buf="";
  function wait(){
    if(!window.emulator||!emulator.add_listener){return setTimeout(wait,500);}
    emulator.add_listener("serial0-output-char",function(c){
      if(c==="\n"){var l=buf.trim();buf="";if(l.indexOf("BLUH:")===0)ask(l.slice(5));}
      else buf+=c;
    });
  }
  async function ask(q){
    var k=localStorage.getItem("bluhkey");
    if(!k){emulator.serial0_send("NOKEY\n");return;}
    try{
      var r=await fetch("https://api.anthropic.com/v1/messages",{method:"POST",
        headers:{"content-type":"application/json","x-api-key":k,"anthropic-version":"2023-06-01","anthropic-dangerous-direct-browser-access":"true"},
        body:JSON.stringify({model:"claude-sonnet-5-5",max_tokens:200,system:"You are BLUH, an obsidian mainframe console. Answer in one short plain-ASCII line.",messages:[{role:"user",content:q}]})});
      var d=await r.json();
      var t=(d.content&&d.content[0]&&d.content[0].text)||"ERR";
      emulator.serial0_send(t.replace(/[^\x20-\x7e]/g," ").slice(0,400)+"\n");
    }catch(e){emulator.serial0_send("NOKEY\n");}
  }
  wait();
  var S=[
   '#!/bin/sh',
   'q="$*"',
   '[ -z "$q" ] && { echo "usage: bluh <question>"; exit; }',
   'echo "=== OBSIDIAN MAINFRAME :: BLUH ==="',
   'stty -F /dev/ttyS0 raw -echo 2>/dev/null',
   'echo "BLUH:$q" > /dev/ttyS0',
   'if read -t 25 a < /dev/ttyS0 && [ "$a" != "NOKEY" ]; then echo "[LLM] $a"; exit; fi',
   'case "$q" in',
   ' *hello*|*hi*) echo "[STUB] GREETINGS, OPERATOR.";;',
   ' *who*) echo "[STUB] I AM BLUH, A 128MB MAINFRAME.";;',
   ' *) echo "[STUB] NO UPLINK. QUERY LOGGED: $q";;',
   'esac'
  ];
  window.sendBluh=function(){
    emulator.keyboard_send_text("cat > /bin/bluh <<'EOF'\n"+S.join("\n")+"\nEOF\nchmod +x /bin/bluh\nclear\necho bluh ready\n");
  };
})();
