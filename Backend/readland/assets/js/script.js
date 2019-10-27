/*document.onload = function () {
    alert(this)
}
*/window.onload = function () {
    //this.alert(window.screen.height)
    d = this.document.getElementById("footer")
    d.style.position= 'relative'
    d.style.top = window.screen.height + 'px';
};
   