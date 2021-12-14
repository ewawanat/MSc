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
            
             //create space for the graph and axes etc:
             const svg = d3.select('.canvas')
                .append('svg')
                  .attr('width', graphWidth + 400 + margin.left + margin.right)
                  .attr('height', graphHeight + margin.top + margin.bottom);

            //set dimensions of graph (with and height)
             const graph = svg.append('g')
                .attr('width', graphWidth)
                .attr('height', graphHeight)
                .attr('transform', `translate(${margin.left}, ${margin.top})`);
               
            // range of x-axis:
             const x = d3.scaleLinear().range([0, graphWidth]);
            // range of y-axis:
             const y = d3.scaleLinear().range([graphHeight, 0]);

             //appending x-axis to the graph
             const xAxisGroup = graph.append('g')
                .attr('class', 'x-axis')
                .attr('transform', `translate(${0}, ${graphHeight})`);
             
                //appending y-axis to the graph
             const yAxisGroup = graph.append('g')
                .attr('class', 'y-axis');


            // create a line:
             const line = d3.line()
                .x(function(d) {
                   return x(d.month) // month is on x-axis
                })
                .y(function(d) {
                   return y(d.frequency)}); //frequency is on y-axis

            // dotted lines for showing connection between x and y axes
             const dottedLines = graph.append('g')
                .attr('class','lines')
                .style('opacity', 0);

            // dotted line coming from x axis
             const xDottedLine = dottedLines.append('line')
                .attr('stroke', 'royalblue')
                .attr('stroke-width', 1)
                .attr('stroke-dasharray', 4)
                .attr('fill', 'royalblue');

            // dotted line coming from y axis
             const yDottedLine = dottedLines.append('line')
                .attr('stroke', 'royalblue')
                .attr('stroke-width', 1)
                .attr('stroke-dasharray', 4)
                .attr('fill', 'royalblue');
            
            //set colours for lines 
             const colour = d3.scaleOrdinal(d3['schemeSet1']);

             //array data contains all information for one species
             var array_data = [];

             //all data contains info for all species
             var all_data = [];
             
            //set containing all unique circles representing frequency 
            const frequencySet = new Set() 

            //push data from python code to all_data:
            data.line_graph_list.forEach(d => {
               d.forEach(index => {
                  all_data.push(index);
               });
            });

            //setting x and y domain (as months and frequency respectively)
            x.domain(d3.extent(data.months, d => d));
            y.domain([0, d3.max(all_data, d => d.frequency)]);   
            
            //creating the path of the graph with lines
             data.line_graph_list.forEach(d => {
                const path = graph.append('path');
                array_data = [];
                   d.forEach(index => {
                      frequencySet.add(index.frequency);  
                      array_data.push(index);
                   });
 
               //sorting the data by month
               array_data.sort((a,b) => a.month - b.month);
                
               //  console.log('array_data');
               //  console.log(array_data);

               // setting fill and colours of the lines:
                path.data([array_data])
                   .attr("fill", 'none')
                   .attr("stroke", d => {
                      console.log("DDDDDDs");
                      console.log(d);   
                      return colour(d[0].species_name)}) // setting colour to be different depending on species name
                   .attr('stroke-width', 2)
                   .attr('d', line);

                });

                // creating circles for intersection of x and y 
                const circles = graph.selectAll('circle')
                   .data(all_data);

                circles.attr('r', circleRadius)
                   .attr('cx', d => x(d.month))
                   .attr('cy', d => y(d.frequency))
                   .attr('fill', 'royalblue');

               //to display all circles in the graph:
                circles.enter()
                   .append('circle')
                         .attr('r', circleRadius)
                         .attr('cx', d => x(d.month))
                         .attr('cy', d => y(d.frequency))
                         .attr('fill', 'royalblue');

               // to make circles appear larger on click
                graph.selectAll('circle')
                   .on('mouseover', (d,i,n) => {
                         d3.select(n[i])
                            .transition().duration(500)
                               .attr('r', circleRadius*2)
                               .attr('fill', 'royalblue')

               // to make x and y dotted lines appear on click:
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
                   //make them disappear when unclicked
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

                   //setting up x axis with months chosen:
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
   
                //formatting ticks for y axis to be unique
                const yAxis = d3.axisLeft(y)
                   .ticks(frequencySet.size)
                   .tickFormat(d3.format("d"));

               //  console.log(frequencySet);
                
                xAxisGroup.call(xAxis);
                yAxisGroup.call(yAxis);

                //settings for x-axis text 
                xAxisGroup.selectAll('text')
                   .attr('transform', 'rotate(-40)')
                   .attr('text-anchor', 'end');
               
                   //setting up legends
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