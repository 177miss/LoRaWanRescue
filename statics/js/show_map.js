
window._AMapSecurityConfig = {
    securityJsCode:"b387593c177d8ef9a4fb9529e7452d6f",
}
src="https://webapi.amap.com/loader.js"
AMapLoader.load({
    key: "1cea1c2420d1bac49d7923c2b0838dbe",       // 申请好的Web端开发者Key，首次调用 load 时必填
    version: "2.0",                 // 指定要加载的 JSAPI 的版本，缺省时默认为 1.4.15
}).then((AMap)=>{
    const map = new AMap.Map('container');
    const marker = new AMap.Marker({
    position:[116.39, 39.9] //位置
})
map.add(marker); //添加到地图
}).catch((e)=>{
    console.error(e);  //加载错误提示
});  