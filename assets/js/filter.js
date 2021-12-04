$("#id_in_country").change(function () {
    const url = $("#displaydataform").attr("data-counties-url");  // get the url of the `load_counties` view
    const countryId = $(this).val();  // get the selected country ID from the HTML input
    $.ajax({                       // initialize an AJAX request
       url: url,                    // set the url of the request (= /enterdata/ajax/load-cities/ )
       data: {
           'country_id': countryId       // add the country id to the GET parameters
       },
       success: function (data) {  
          var list = document.getElementById("id_in_county");
          list.innerHTML = ""; //clear all 
          let html_data; //= '<option value="">----Select county/counties---</option>';
          data.forEach(function (county) {
             html_data +=`<option value = "${county.name}"> ${county.name} </option>`
          });
          list.innerHTML = html_data; 
       } 
   });
});