// note uses userChecked from markUsers.js (coffee)

function refreshVis() {
  if (userdata != []) {

    OPTS = getOptions();
    clearTokenBox();//Sriram:Added this to clear infoBox First 
    //Opts for Line
    var shadeOptsL = document.getElementById("shadeOpts_L");
    var shadeStateL = shadeOptsL.options[shadeOptsL.selectedIndex].value;

    var widthOptsL = document.getElementById("widthOpts_L");
    var widthStateL = widthOptsL.options[widthOptsL.selectedIndex].value;
    //Opts for Dot
    var shadeOptsD = document.getElementById("shadeOpts_D");
    var shadeStateD = shadeOptsD.options[shadeOptsD.selectedIndex].value;

    var widthOptsD = document.getElementById("widthOpts_D");
    var widthStateD = widthOptsD.options[widthOptsD.selectedIndex].value;


    var lineChecked = document.getElementById('showLines').checked;
    var dotChecked = document.getElementById('showDots').checked;
    var groupChecked = document.getElementById('colorByGroup').checked;

    OPTS.lineChecked = lineChecked;
    OPTS.dotChecked = dotChecked;
    OPTS.groupChecked = groupChecked;

    OPTS.lineColNoneChecked_s_l = shadeStateL == "none_s_l";
    OPTS.lineColMoveChecked_s_l = shadeStateL == "moveCount_s_l";

    OPTS.lineColNoneChecked_t_l = widthStateL == "none_t_l";
    OPTS.lineColMoveChecked_t_l = widthStateL == "moveCount_t_l";

    OPTS.dotColNoneChecked_s_d = shadeStateD == "none_s_d";
    OPTS.dotColAccChecked_s_d = shadeStateD == "accuracy_s_d";

    OPTS.dotRadNoneChecked_t_d = widthStateD == "none_t_d";
    OPTS.dotRadAccChecked_t_d = widthStateD == "accuracy_t_d";

    drawVis(userdata, "#VIS", 800, 800, OPTS);
  }
}

VisData = {}; // allow access to the data for thevis
var dClrsUsers = {};


function drawVis(userdata, anchorname, W, H, OPTS) {
    //var bDrawLines = OPTS['DrawLines'];
    //var bDrawEndPoints = OPTS['DrawEndPoints'];
    //var bDrawDiamonds = OPTS['DrawDiamonds'];
    //var bDrawArrows = OPTS['DrawArrows'];
colorPallet = ["#2dfefe", "#0a72ff", "#1eff06", "#ff1902", "#827c01", "#fe07a6", "#a8879f", "#fcff04", "#c602fe", "#16be61", "#ff9569", "#05b3ff", "#ecffa7", "#3f8670", "#e992ff", "#ffb209", "#e72955", "#83bf02", "#bba67b", "#fe7eb1", "#7570c1", "#85bfd1", "#f97505", "#9f52e9", "#8ffec2", "#dad045", "#b85f60", "#fe4df2", "#75ff6c", "#78a55a", "#ae6a02", "#bebeff", "#ffb3b3", "#a4fe04", "#ffc876", "#c548a7", "#d6492b", "#547da7", "#358b06", "#95caa9", "#07b990", "#feb6e9", "#c9ff76", "#02b708", "#7b7a6e", "#1090fb", "#a46d41", "#09ffa9", "#bb76b7", "#06b5b6", "#df307c", "#9b83fd", "#ff757c", "#0cd9fd", "#bdba61", "#c89d26", "#91df7e", "#108c49", "#7b7d40", "#fdd801", "#048699", "#fc9d40", "#ff0f3b", "#87a72c", "#a25cc2", "#b95a82", "#bb8a80", "#cce733", "#f7b58d", "#adaaab", "#c141c8", "#08fbd8", "#ff6de4", "#c26040", "#bb9bf6", "#b08f44", "#6d96de", "#8dcaff", "#5be51c", "#68c948", "#ff5fb8", "#7f9872", "#9aa5ca", "#bad292", "#c32fe4", "#fc92df", "#e08eaa", "#fd0afd", "#2daad4", "#d96d2a", "#69e0c9", "#ce4b69", "#79ca8d", "#6e8e9a", "#ffec83", "#de0fb5", "#8471a2", "#bbd766", "#e94805", "#06ff54", "#9cf046", "#6a63ff", "#05e774", "#e38c7b", "#f6ff75", "#3cda96", "#d68e4b", "#d774fe", "#feca4c", "#80ff95", "#5571e1", "#6da9a1", "#a5a20d", "#d5484a", "#688326", "#e7d08f", "#4e8653", "#5cad4c", "#c19bcf", "#ff0e76", "#d3ff0b", "#a66877", "#6ddde3", "#a544fe", "#c2fdb5", "#8f7955", "#fd735b", "#8497fd", "#fd919d", "#fdf346", "#fe5581", "#fd4e50", "#0ca82e", "#d4a8b2", "#d14e91", "#0d9069", "#0c8bca", "#fd9403", "#d5b401", "#adc32e", "#efacfe", "#9da668", "#57b093", "#787791", "#ff6f39", "#9e790a", "#d18903", "#abb49a", "#a06790", "#cf70cb", "#c8fe96", "#488834", "#dcbf55", "#e82f23", "#9a90d5", "#9cd54d", "#c7936c", "#05dc4a", "#98f372", "#907275", "#167dcf", "#db2b9f", "#16b16e", "#49a802", "#66cd1d", "#905fdc", "#cecd02", "#a376ca", "#939540", "#a7e103", "#d9ac6e", "#099334", "#db7701", "#3facbd", "#a0cb76", "#6aa3d5", "#dcaf98", "#b6692e", "#a76a59", "#04908e", "#d771ab", "#a69683", "#8268d0", "#72ab79", "#f70c8b", "#ebaa4c", "#9ce7b8", "#5f837a", "#df708c", "#ad9c32", "#39ffc2", "#d28388", "#79d5f9", "#e35eff", "#ffaf72", "#55e0b3", "#e8c0fe", "#6a69ed", "#fe07d3", "#0c86af"];

    var dotdata = userDots(userdata);
    var linedata = userLines(userdata);
    VisData.dotdata = dotdata;
    VisData.linedata = linedata;

    var getX = function(d) {return d.x;},
        getY = function(d) {return d.y;},
        dotXs = dotdata.map(getX),
        dotYs = dotdata.map(getY);
    
    dUserGroup = {0:1, 1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1,10:1,11:1,12:6,
                 13:6, 14:6, 15:6, 16:6, 17:6, 18:6, 19:6, 20:6, 21:6, 22:6, 23:6};
    //dUserGroupAltColors = {1:1, 5:2, 6:3, 8:4, 9:5, 10:6, 2:7, 4:8, 7:9, 11:10};

    if(!OPTS.groupChecked){
    //var fClrsUsers = d3.scale.category20();
    dClrsUsers = colorPallet;

    for (var key in dUserGroup){
      var userNumber = ".u"+key;
      //var childText = "<div style='background:'"
      var selectNode = d3.selectAll(".opt").filter(userNumber)
                .style("border-radius","2px")
                .style("background",dClrsUsers[key]);

    }
    }

    if(OPTS.groupChecked){//Sriram: if group is checked color selection process:
    

    //var fClrsUsers = d3.scale.category20();
    dClrsUsers = colorPallet;
     for (var key in dUserGroup){
      var userNumber = ".u"+key;
      //var childText = "<div style='background:'"
      var selectNode = d3.selectAll(".opt").filter(userNumber)
                .style("border-radius","2px")
                .style("background",dClrsUsers[dUserGroup[key]]);

    }

    }

    var xOffset = 10, yOffset = 10,
        dotDiam = 6, lineThick = 4;
    
    // functions from data space to vis space
    var fScaleX = d3.scale.linear()
                          .domain([Math.min.apply(null, dotXs),
                                   Math.max.apply(null, dotXs)])
                          .range([0, W-2*xOffset]);
    var fScaleY = d3.scale.linear()
                          .domain([Math.min.apply(null, dotYs),
                                   Math.max.apply(null, dotYs)])
                          .range([0, H-2*yOffset]);

    // functions combining data->vis space fcns with getX or getY
    var fGetScaledX = function(d){return fScaleX(getX(d)) + xOffset;},
        fGetScaledY = function(d){return fScaleY(getY(d)) + yOffset;}

    var divTooltip = d3.select("body").append("div")
                                      .attr("class", "tooltip")
                                      .style("opacity", 0)
                                      .style("position", "absolute")
                                      .style("width", "200px")
                                      .style("background-color", "#ee0")
                                      .style("pointer-events", "none")
                                      .style("padding","8px") //Sriram: Added this to include some padding on the boxes
                                      .style("border-radius","10px");//Sriram: Added this to have rounded corners on the info boxes

    var svg = d3.select(anchorname)
      //.append("g") // svg group and .call are for zooming
      .call(d3.behavior.zoom()
	    .x(fScaleX)
            .y(fScaleY)
            .scaleExtent([1, 80])
            .on("zoom", fZoom));

    svg.append("rect") // background rect means zoom affects whole area
      .attr("width", W) //W:800px, H:800px
      .attr("height", H)
      .attr("fill", "transparent")


    // remove old dots and lines
    svg.selectAll(".dot").remove();
    svg.selectAll(".line").remove();
    svg.selectAll(".cross").remove();

    // filter data by users checked off
    dotdata = dotdata.filter( function(x){return userChecked(x.user);});
    linedata = linedata.filter( function(x){return userChecked(x.user);});
    
    // draw the lines
    var lineFunction = d3.svg.line()
       .x(function(d) { return fGetScaledX(d) ; })
       .y(function(d) { return fGetScaledY(d) ; })
       .interpolate("cardinal");
    var fTwoSegments = function(ld) { // turn one linedatum into 2 fTwoSegmentsnts
       return [ { x:ld.x1, y:ld.y1 },
                halfwayBump(ld, ld['backward']),
                //{ x:ld.x1 + (ld.x2-ld.x1)/2, y:ld.y1 + (ld.y2-ld.y1)/2 },
                { x:ld.x2, y:ld.y2 } ];
    };
    var lines = svg.selectAll(".line")
       .data(linedata)
       .enter().append("path")
       .attr("class", function(d){return "line user" + d.user;})
      //.attr("d", function(d){return lineFunction(fTwoSegments(d));})
       .attr("stroke", function(d) {
	       if (d.customColor) {
		 return d.customColor;
               } else 
          { if(OPTS.lineColNoneChecked_s_l){if(OPTS.groupChecked){return dClrsUsers[dUserGroup[d.user]];}else{return dClrsUsers[d.user];}}
            if(OPTS.lineColMoveChecked_s_l){colVal = Math.round(255/90 * (80-d.count));return d3.rgb(colVal,colVal,colVal); }
            if(OPTS.groupChecked){return dClrsUsers[dUserGroup[d.user]];}
          } })
       .attr("stroke-width", function(d){ //Sriram:Added this to accomadate varying line width based on read count
            if(OPTS.lineColNoneChecked_t_l){return lineThick;}
            if(OPTS.lineColMoveChecked_t_l){return 2.5+d.count/8;}
             })
       .attr("marker-mid", "url(#inlineMarker)")
       .style("fill", "transparent")
       .on("click", function(d) { updateInfoBox(d.info);
                                  updateSharedTokens(d.info, 'line'); })
       .on("mouseover", function(d) {
              divTooltip.transition()
                   .duration(200)
                   .style("opacity", .9);
              divTooltip.html(d.info + "<br/>")
                     .style("left", (d3.event.pageX + 5) + "px")
                     .style("top", (d3.event.pageY - 28) + "px");
              divTooltip.style("background-color", dClrsUsers[d.user]);
	   })
       .on("mouseout", function(d) {
              divTooltip.transition()
                   .duration(500)
                   .style("opacity", 0);
           })

    if(!OPTS.lineChecked){svg.selectAll(".line").remove();} //Sriram: added this to remove lines with lineChecked is not checked.


    // draw dots
    var dots = svg.selectAll(".dot")
       .data(dotdata)
       .enter().append("circle")
       .attr("class", function(d){str = d.info;
                                    //DFNo = str.slice(17,19);
                                    return "dot user" + d.user;// +" DF"+ DFNo;
                                    
                            //      return "dot user" + d.user;
                                 })
       .attr("r", function(d){
            if(OPTS.dotRadNoneChecked_t_d){return dotDiam;}
            if(OPTS.dotRadAccChecked_t_d){return 31.5*Math.sqrt(d.acc-0.88);} //Sriram: dynamic radius (lowest acc value was around 0.88)}
       })
      // .attr("cx", fGetScaledX)
      // .attr("cy", fGetScaledY)
      .style("fill", function(d) {
	               if (d.customColor) {
		         return d.customColor;
                       } else { 
          if(OPTS.dotColNoneChecked_s_d){if(OPTS.groupChecked){return dClrsUsers[dUserGroup[d.user]];}else{return dClrsUsers[d.user];} }
          if(OPTS.dotColAccChecked_s_d){colVal = 255-Math.round(255*(d.acc-0.895)*8.5); return d3.rgb(colVal, colVal, colVal);}
          if(OPTS.groupChecked){return dClrsUsers[dUserGroup[d.user]];}} 
      })  
       .on("click", function(d) { updateInfoBox(d.info);
                                  //newDfInfo = d.info.slice(24,9999999) //Sriram: Adding this to ignore "Top key words"
                                  updateSharedTokens(newDfInfo, 'dot'); 
                                  str = d.info; console.log(str);
                                  //tempDFNo = str.slice(17,19);
                                  tempName = ".dot.user" + d.user;//+".df"+tempDFNo; console.log(tempName); //creating temp identifier
                                  svg.selectAll(tempName)
                                      //.attr('r',12)
                                      //.style("fill", "transparent")       
                                      //.style("stroke", "red");  
                                      //.attr('r',100)
                                      .style('fill',d3.rgb('blue')); //Sriram:changes the color to blue upon click
                                    })
       .on("mouseover", function(d) {
               divTooltip.transition()
                    .duration(200)
                    .style("opacity", .9);
               divTooltip.html("<b style='font-size:20px;'>User " + d.user + "</b>"+
 			      d.info)
                      .style("left", (d3.event.pageX + 5) + "px")
                      .style("top", (d3.event.pageY - 28) + "px");
               divTooltip.style("background-color", dClrsUsers[d.user]);
           })
       .on("mouseout", function(d) {
               divTooltip.transition()
                    .duration(500)
                    .style("opacity", 0);
           })
       .attr("transform", fTransform);

    if(!OPTS.dotChecked){svg.selectAll(".dot").remove();}//Sriram: added this to remove dots when dotChecked is not checked.

   // add a cross at the starting point
    // **** don't do this if no dotdata
    //   create a transform function for the origin (for zoom)
    var fOriginTransform = function() { 
       return "translate(" + fGetScaledX(dotdata[0]) + "," + fGetScaledY(dotdata[0]) + ")";
    };
    var cross1 = svg.append("line") // upper left to lower right
       .attr("class","cross")
       .attr("x1", -5)
       .attr("y1", -5)
       .attr("x2", 5)
       .attr("y2", 5)
       .style("stroke", d3.rgb(0,0,0))
       .style("stroke-width", 4)
       .attr("transform", fOriginTransform);
    var cross2 = svg.append("line") // upper left to lower right
       .attr("class","cross")
       .attr("x1", 5)
       .attr("y1", -5)
       .attr("x2", -5)
       .attr("y2", 5)
       .style("stroke", d3.rgb(0,0,0))
       .style("stroke-width", 4)   
       .attr("transform", fOriginTransform);
    

    fZoom(lines); // initial positioning calculation
  
    function fZoom() {
        dots.attr("transform", fTransform);
        //lines.attr("transform", fTransformLine);
        cross1.attr("transform", fOriginTransform);
        cross2.attr("transform", fOriginTransform);
        svg.selectAll(".line")
           .attr("d",  function(d){return lineFunction(fTwoSegments(d));});
    }


    function fTransform(d) {
      return "translate(" + fGetScaledX(d) + "," + fGetScaledY(d) + ")";
    }

}
