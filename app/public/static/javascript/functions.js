function filter(){
    var state = document.getElementById("filter").style.display;

    if (state == "none"){
        document.getElementById("filter").style.display = "flex" 
    }

    else{
        document.getElementById("filter").style.display = "none"    
    }
    
}
function goBack(){
    window.history.back()

}