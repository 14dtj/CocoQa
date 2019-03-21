/**
 * Created by flyboss on 2018/12/31.
 */
function KB(nodes, d3id) {
    this.nodes = nodes;
    var edges = new Array();
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].type === "1") {
            centerEntityIndex = i;
            break;
        }
    }
    for (var i = 0; i < nodes.length; i++) {
        if (i != centerEntityIndex) {
            edges.push(new Object({source: centerEntityIndex, target: i, relation: nodes[i].relation}));
        }
    }

    //当鼠标移到实体上展示其名字
    var tooltip = d3.select("#" + d3id)
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("width", "130px")
        .style("word-break", "normal")
        .style("white-space", "normal")
        .style("visibility", "hidden");

    var width = 700;
    var height = 500;

    var svg = d3.select("#" + d3id)
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    var force = d3.layout.force()
        .nodes(nodes)		//指定节点数组
        .links(edges)		//指定连线数组
        .size([width, height])	//指定范围
        .linkDistance(function (d, i) {
            if (d.target.type === "2") {
                return 200;
            } else {
                return 200;
            }
        })	//指定连线长度
        .charge(-1500);	//相互之间的作用力

    force.start();	//开始作用

//添加节点
    var svg_nodes = svg.selectAll("circle")
        .data(nodes)
        .enter()
        .append("circle")
        .attr("r", function (d, i) {
            if (d.type === "1") {
                return 30;
            } else if (d.type === "2") {
                return 25;
            } else {
                return 25;
            }
        })
        .attr("id", function (d, i) {
            if (d.type === "1") {
                return d3id + "centerEntity";
            } else if (d.type === "2") {
                return d3id + "otherEntity";
            } else {
                return d3id + "property";
            }
        })
        .style("fill", function (d, i) {
            if (d.type === "1") {
                return "#1f77b4";
            } else if (d.type === "2") {
                return "#ffbb78";
            } else {
                return "#ff9896";
            }
        })
        .on("dblclick", function (d, i) {
            clickMainEntity(d);
        })
        .on("mouseover", function (d, i) {
            tooltip.text(d.name);
            svg.selectAll("#" + d3id + i + "name").style("visibility", "hidden");
            return tooltip.style("visibility", "visible");
        })
        .on("mousemove", function () {
//            console.log(this)
            return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px");
            // return tooltip.style("top", (this.x - 10) + "px").style("left", (this.y + 10) + "px");
        })
        .on("mouseout", function (d, i) {
            svg.selectAll("#" + d3id + i + "name").style("visibility", "visible");
            return tooltip.style("visibility", "hidden");
        })
        .call(force.drag);	//使得节点能够拖动


    //添加描述节点的文字
    var svg_texts = svg.selectAll("text")
        .data(nodes)
        .enter()
        .append("text")
        .attr("class", function (d, i) {
            if (d.type === "2") {
                return d3id + "otherEntityName";
            } else if (d.type === "3") {
                return d3id + "propertyName";
            }
        })
        .attr("id", function (d, i) {
            return d3id + i + "name";
        })
        .attr("dx", 0)
        .attr("dy", 5)
        .text(function (d) {
            return d.name.substr(0,20);
        });

    //添加连线
    var svg_edges = svg.selectAll("edgepath")
        .data(edges)
        .enter()
        .append("path")
        .attr({
            'd': function (d) {
                return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y
            },
            'id': function (d, i) {
                if (d.target.type === "2") {
                    return d3id + "otherEntityLine";
                } else if (d.target.type === "3") {
                    return d3id + "propertyLine";
                }
            }
        })
        .style("stroke", function (d) {
            var lineColor;
            lineColor = "#B43232";
            return lineColor;
        })
        .style("pointer-events", "none")
        .style("stroke-width", 0.5)
        .attr("marker-end", "url(#resolved)");

    //添加连线文字
    var svg_text = svg.append("g").selectAll("edgelabel")
        .data(edges)
        .enter()
        .append("text")
        .style("pointer-events", "none")
        .attr({
            'id': function (d, i) {
                if (d.target.type === "2") {
                    return d3id + "otherEntityLineText";
                } else if (d.target.type === "3") {
                    return d3id + "propertyLineText";
                }
            },
            'dx': 50,
            'dy': 0
        });

    svg_text.append('textPath')
        .attr('xlink:href', function (d, i) {
            return '#edgepath' + d3id + i
        })
        .style("pointer-events", "none")
        .text(function (d) {
            return d.relation;
        });

    force.on("tick", function () {	//对于每一个时间间隔
        //更新节点坐标
        svg_nodes.attr("cx", function (d) {
            return d.x;
        })
            .attr("cy", function (d) {
                return d.y;
            });

        svg_edges.attr('d', function (d) {
            var path = 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
            return path;
        });

        svg_text.attr('transform', function (d, i) {
            if (d.target.x < d.source.x) {
                bbox = this.getBBox();
                rx = bbox.x + bbox.width / 2;
                ry = bbox.y + bbox.height / 2;
                return 'rotate(180 ' + rx + ' ' + ry + ')';
            }
            else {
                return 'rotate(0)';
            }
            // return 'dx: 50';
        });

        //更新节点文字坐标
        svg_texts.attr("x", function (d) {
            return d.x;
        })
            .attr("y", function (d) {
                return d.y;
            });
    });

    var flag = 1;

    function clickMainEntity(d) {
        //type=1时说明点击了当前实体，根据flag展示相关实体或属性
        if (d.type === "1") {
            //隐藏属性
            if (flag === 1) {
                flag = 0;
                d3.selectAll("#" + d3id + "otherEntity").style("visibility", "hidden");
                d3.selectAll("#" + d3id + "otherEntityLine").style("visibility", "hidden");
                d3.selectAll("#" + d3id + "otherEntityLineText").style("visibility", "hidden");
                d3.selectAll("." + d3id + "otherEntityName").style("visibility", "hidden");
                d3.selectAll("#" + d3id + "property").style("visibility", "visible");
                d3.selectAll("#" + d3id + "propertyLine").style("visibility", "visible");
                d3.selectAll("#" + d3id + "propertyLineText").style("visibility", "visible");
                d3.selectAll("." + d3id + "propertyName").style("visibility", "visible");
            } else {
                flag = 1;
                d3.selectAll("#" + d3id + "otherEntity").style("visibility", "visible");
                d3.selectAll("#" + d3id + "otherEntityLine").style("visibility", "visible");
                d3.selectAll("#" + d3id + "otherEntityLineText").style("visibility", "visible");
                d3.selectAll("." + d3id + "otherEntityName").style("visibility", "visible");
                d3.selectAll("#" + d3id + "property").style("visibility", "hidden");
                d3.selectAll("#" + d3id + "propertyLine").style("visibility", "hidden");
                d3.selectAll("#" + d3id + "propertyLineText").style("visibility", "hidden");
                d3.selectAll("." + d3id + "propertyName").style("visibility", "hidden");
            }
        } else if (d.type === "2") {
            //点击了相关实体，应当跳转到相关实体上去
            $("#answer").empty();
            var question = {"url": d.Id};
            $.ajax({
                type: 'POST',
                url: address + "/accurate",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                data: JSON.stringify(question),
                success: function (result) {
                    var json = result.data;
                    displayEntity(json);
                    Prism.highlightAll();
                },
                failure: function (result) {
                    alert(result);
                },
                error: function (result) {
                    alert(result);
                }
            });
        }
    }


    //添加图例，说明每个点的意义
    addMyLegend();
    function addMyLegend() {
        var legendInfo = [
            {"name": "center entity", "color": "#1f77b4"},
            {"name": "related entity", "color": "#ffbb78"},
            {"name": "property", "color": "#ff9896"}];
        var legend = svg.selectAll(".legend")
            .data(legendInfo)//seriesNames.slice().reverse()
            .enter().append("g")
            .attr("class", "legend");

        legend.append("circle")
            .attr("cx", function (d, i) {
                return 30 + 120 * i;
            })
            .attr("cy", function (d, i) {
                return 20;
            })
            .attr("r", function (d) {
                return 8;
            })
            .data(legendInfo)
            .style("fill", function (d, i) {
                return legendInfo[i].color;
            });


        legend.append("text")
            .data(legendInfo)
            .attr("x", function (d, i) {
                return 40 + 120 * i;
            })
            .attr("y", function (d, i) {
                return 25;
            })
            .text(function (d, i) {
                return legendInfo[i].name;
            });
//        console.log(legend);
    }
}

