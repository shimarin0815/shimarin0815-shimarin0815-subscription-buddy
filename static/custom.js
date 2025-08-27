async function requestNotify(){
  if(!("Notification" in window)) { alert("このブラウザは通知に対応していません"); return; }
  const perm = await Notification.requestPermission();
  if(perm === "granted"){
    new Notification("通知が有効になりました 🎉");
  }
}
// 例：ページロード時、リマインド対象があれば軽く通知（サーバ側で判定してもOK）
document.addEventListener("DOMContentLoaded", ()=>{
  const box = document.querySelector("[data-has-remind]");
  if(box && Notification.permission==="granted"){
    new Notification("サブスク管理くん", { body: "支払い/無料終了が近い項目があります！" });
  }
});
