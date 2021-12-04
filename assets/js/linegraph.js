$(document).ready(function() {
    $("#linegraph").click(function() {
       var formdata = {
          species: $("#id_species_name").val(),
          country:$("#id_in_country").val(),
          county: $("#id_in_county").val(),
          from_date: $("#id_from_date").val(),
          to_date: $("#id_to_date").val(),
       }
       $.ajax({
          type:'POST',
          url:'create_linegraph/',
          data: formdata,
          success: function(data){
             console.log(data)
             const margin = { top: 40, right: 20, bottom: 50, left: 100 };
             const graphWidth = 560 - (margin.left + margin.right);
             const graphHeight = 400 - (margin.top + margin.bottom);
             const circleRadius = 4;

             const svg = d3.select('.canvas')
                .append('svg')
                  .attr('width', graphWidth + 400 + margin.left + margin.right)
                  .attr('height', graphHeight + margin.top + margin.bottom);

             const graph = svg.append('g')
                .attr('width', graphWidth)
                .attr('height', graphHeight)
                .attr('transform', `translate(${margin.left}, ${margin.top})`);
               

             const x = d3.scaleLinear().range([0, graphWidth]);
             const y = d3.scaleLinear().range([graphHeight, 0]);

             const xAxisGroup = graph.append('g')
                .attr('class', 'x-axis')
                .attr('transform', `translate(${0}, ${graphHeight})`);

             const yAxisGroup = graph.append('g')
                .attr('class', 'y-axis');



             const line = d3.line()
                .x(function(d) {
                   return x(d.month)
                })
                .y(function(d) {
                   return y(d.frequency)});

             const dottedLines = graph.append('g')
                .attr('class','lines')
                .style('opacity', 0);

             const xDottedLine = dottedLines.append('line')
                .attr('stroke', 'royalblue')
                .attr('stroke-width', 1)
                .attr('stroke-dasharray', 4)
                .attr('fill', 'royalblue');

             const yDottedLine = dottedLines.append('line')
                .attr('stroke', 'royalblue')
                .attr('stroke-width', 1)
                .attr('stroke-dasharray', 4)
                .attr('fill', 'royalblue');

             const colour = d3.scaleOrdinal(d3['schemeSet1']);

             var array_data = [];
             var all_data = [];
             
            const frequencySet = new Set() 

            data.line_graph_list.forEach(d => {
               d.forEach(index => {
                  all_data.push(index);
               });
            });

            x.domain(d3.extent(data.months, d => d));
            y.domain([0, d3.max(all_data, d => d.frequency)]);   
            

             data.line_graph_list.forEach(d => {
                const path = graph.append('path');
                array_data = [];
                   d.forEach(index => {
                      frequencySet.add(index.frequency);  
                      array_data.push(index);
                   });
 
               
               array_data.sort((a,b) => a.month - b.month);
                
                console.log('array_data');
                console.log(array_data);

                path.data([array_data])
                   .attr("fill", 'none')
                   .attr("stroke", d => {
                      console.log("DDDDDDs");
                      console.log(d);   
                      return colour(d[0].species_name)})
                   .attr('stroke-width', 2)
                   .attr('d', line);

                });

                const circles = graph.selectAll('circle')
                   .data(all_data);

                circles.attr('r', circleRadius)
                   .attr('cx', d => x(d.month))
                   .attr('cy', d => y(d.frequency))
                   .attr('fill', 'royalblue');

                circles.enter()
                   .append('circle')
                         .attr('r', circleRadius)
                         .attr('cx', d => x(d.month))
                         .attr('cy', d => y(d.frequency))
                         .attr('fill', 'royalblue');

                graph.selectAll('circle')
                   .on('mouseover', (d,i,n) => {
                         d3.select(n[i])
                            .transition().duration(500)
                               .attr('r', circleRadius*2)
                               .attr('fill', 'royalblue')

                         xDottedLine
                            .attr('x1', x(d.month))
                            .attr('x2', x(d.month))
                            .attr('y1', graphHeight)
                            .attr('y2', y(d.frequency));

                         yDottedLine
                            .attr('x1', 0)
                            .attr('x2', x(d.month))
                            .attr('y1', y(d.frequency))
                            .attr('y2', y(d.frequency));

                         dottedLines.style('opacity', 1);
                   })
                   .on('mouseleave', (d,i,n) => {
                         d3.select(n[i])
                            .transition().duration(500)
                               .attr('r', circleRadius)
                               .attr('fill', 'royalblue');
                   
                         dottedLines.style('opacity', 0);
                   });


             // console.log('array_data');
             // console.log(array_data);
             // console.log(data);
             // console.log("data.line_graph_list")
             // console.log(data.line_graph_list)
             // console.log("d")
             // console.log(d)


                const xAxis = d3.axisBottom(x)
                   .ticks(data.months.length)
                   .tickFormat(d => {
                    switch(d) {
                        case 1:
                            return "January";
                            break;
                        case 2:
                            return "February";
                            break;
                        case 3:
                            return "March";
                            break;
                        case 4:
                           return "April";
                            break;
                        case 5:
                            return "May";
                            break;;
                        case 6:
                            return "June";
                            break;
                        case 7:
                            return "July";
                            break;
                        case 8:
                            return "August";
                            break;
                        case 9:
                            return "September";
                            break; 
                        case 10:
                            return "October";
                            break; 
                        case 11:
                            return "November";
                            break;  
                        default:                              
                            return "December";
                        } 
                });
   
                const yAxis = d3.axisLeft(y)
                   .ticks(frequencySet.size)
                   .tickFormat(d3.format("d"));

                console.log(frequencySet);
                
                xAxisGroup.call(xAxis);
                yAxisGroup.call(yAxis);

                xAxisGroup.selectAll('text')
                   .attr('transform', 'rotate(-40)')
                   .attr('text-anchor', 'end');

                   var legend = svg.selectAll('.legend')
                   .data(colour.domain())
                   .enter()
                   .append('g')
                   .attr('class', 'legend')
                   .attr('transform', function(d, i) {
                     return `translate(${graphWidth + 140}, ${40 + i * 30})`;
                   });

                legend.append('rect')
                   .attr('width', 20)
                   .attr('height', 1)
                   .style('fill', colour)
                   .style('stroke', colour);
                 
                legend.append('text')
                   .attr('x', 25)
                   .attr('y', 5)
                   .text(d => d)
                   .attr('fill', colour);
            }
      });
   });
});