function live_search(value){
    value = value.trim(); 
    if(value != "") { 
        $.ajax({
            url: "search",
            data: {search_text: value},
            dataType: "json",
            success: function(data){
                let res = "";
                for(i in data.results){
                    res += 
                    `
                    <div>
                        ${data.results[i]}
                    </div>
                    `;
                }
                $("#results").html(res);
            }
        });
    }
    else {
        $("#results").html("");
    }
}