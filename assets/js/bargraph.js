$(document).ready(function() {
    $("#bargraph").click(function() {
       var formdata = {
          species: $("#id_species_name").val(),
          country:$("#id_in_country").val(),
          county: $("#id_in_county").val(),
          from_date: $("#id_from_date").val(),
          to_date: $("#id_to_date").val(),
          }
       $.ajax({
          type:'POST',
          url:'create_bargraph/',
          data: formdata,
          success: function(data){
          console.log(data)
          const width = 1500;
          const height = 650;
          const margin = { top: 50, bottom: 250, left: 40, right: 30 };

          const svg = d3.select('#d3-container')
          .append('svg')
          .attr('width', width - margin.left - margin.right)
          .attr('height', height - margin.top - margin.bottom)
          .attr("viewBox", [0, 0, width, height]);

          const x = d3.scaleBand()
          .domain(d3.range(data.length))
          .range([margin.left, width - margin.right])
          .padding(0.1)


          const y = d3.scaleLinear()
          .domain([0, d3.max(data, d=> d.frequency)])
          .range([height - margin.bottom, margin.top])

          svg
          .append("g")
          .attr("fill", 'royalblue')
          .selectAll("rect")
          .data(data.sort((a, b) => d3.descending(a.frequency, b.frequency)))
          .join("rect")
             .attr("width", x.bandwidth())
             .attr("height", 0)
             .attr("x", (d, i) => x(i))
             .attr('title', (d) => d.frequency)
             .attr("class", "rect")
             .attr("y", height)
             .transition().duration(500)
                .attr("y", d => y(d.frequency))
                .attr("height", d => y(0) - y(d.frequency));

          function yAxis(g) {
          g.attr("transform", `translate(${margin.left}, 0)`)
             .call(d3.axisLeft(y)
             .ticks(5, data.format)
             .tickFormat(d=> d + ' birds'))
             .attr("font-size", '20px');
          }

          function xAxis(g) {
          g.attr("transform", `translate(0,${height - margin.bottom})`)
             .call(d3.axisBottom(x)
             .tickFormat(i => data[i].species_name))
             .attr("font-size", '20px')
          g.selectAll('text')
             .attr('transform', 'rotate(-40)')
             .attr('text-anchor', 'end')   
          }

          svg.append("g").call(xAxis);
          svg.append("g").call(yAxis);
          svg.node();
          }
       });
    });
 });