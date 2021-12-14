$("#id_in_country").change(function () {
    const url = $("#enterdataform").attr("data-counties-url");  // get the url of the `load_counties` view
    const countryId = $(this).val();  // get the selected country ID from the HTML input
    console.log(url);
    console.log(countryId);
    $.ajax({                       // initialize an AJAX request
       url: url,                    // set the url of the request (= /enterdata/ajax/load-counties/ )
       data: {
           'country_id': countryId       // add the country id to the GET parameters
       },
       success: function (data) {  
          console.log(data);
          var list = document.getElementById("id_in_county");
          console.log(list);
          list.innerHTML = ""; //clear all 
          let html_data = '<option value="">---------</option>';
          data.forEach(function (county) {
             console.log(county);
             html_data +=`<option value = "${county.name}"> ${county.name} </option>`
          });
          list.innerHTML = html_data; 
       }
   });
 });