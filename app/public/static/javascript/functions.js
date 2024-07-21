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

function distribution_platform(data){
    let values_array = [];
    let labels_array = [];
    let json_data = JSON.parse(data)
    for(let i=0;i<json_data.elements.length;i++){
        labels_array.push(json_data.elements[i].platform);
        values_array.push(json_data.elements[i].number);
    }

  
    var data = [{
        values: values_array,
        labels: labels_array,
        type: 'pie',
        textinfo: "label+percent",
        textposition: "inside",
      }];
      
      var layout = {
        title: "Distribucion por plataforma",
        showlegend: false,
        autosize:true,
        margin: {"t": 30, "b": 0, "l": 0, "r": 0},
        height: 500,
        width: 400
      };
      
      Plotly.newPlot('platform_dist', data, layout,{displayModeBar: false});
      

}