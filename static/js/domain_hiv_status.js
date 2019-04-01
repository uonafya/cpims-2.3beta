$(document).ready(function() {

    var hiv_positive = parseInt($('[name="hiv_positive_f"]').val());
    var HIV_positive_on_arv = parseInt($('[name="HIV_positive_on_arv_f"]').val());
    var HIV_positive_not_on_arv = parseInt($('[name="HIV_positive_not_on_arv-f"]').val());
    var HIV_negative = parseInt($('[name="HIV_negative_f"]').val());
    var HIV_unknown_status = parseInt($('[name="HIV_unknown_status_f"]').val());

    var hiv_positive = parseInt($('[name="hiv_positive_m"]').val())
    var HIV_positive_on_arv = parseInt($('[name="HIV_positive_on_arv_m"]').val())
    var HIV_positive_not_on_arv = parseInt($('[name="HIV_positive_not_on_arv_m"]').val())

    var HIV_negative = parseInt($('[name="HIV_negative_m"]').val())
    var HIV_unknown_status =parseInt($('[name="HIV_unknown_status_m"]').val())

    add_ovc_domain_hiv_status();
    add_ovc_domain_hiv_status_negative();

	function add_ovc_domain_hiv_status(){
			var ticksLabel = [
				[0, "HIV+"], [1, "HIV+ <br/> on ARV"], [2, "HIV+ NOT <br/> on ARV"]
			];

            var options = {
				xaxis: {  tickColor: 'transparent',  ticks: ticksLabel},
				grid: {
					hoverable: true,
					tickColor: "#ccc",
					borderWidth: 0,
					borderColor: 'rgba(0,0,0,0.2)'
				},
				series: {
					stack: true,
					lines: { show: false, fill: false, steps: false },
					bars: {
						show: true,
						align: 'center',
						fillColor: null,
						barWidth: 0.5
					},
					highlightColor: 'rgba(0,0,0,0.8)'
				},
				legend: {
					show: false
				 }
			};


            function showTooltip3(x, y, contents) {
                $('<div id="tooltip3" class="flot-tooltip">' + contents + '</div>').css( {
                    top: y,
                        left: x + 35
                    }).appendTo("body").fadeIn(200);
                }


            var hiv_positive_f = [[0, hiv_positive]] ;
            var HIV_positive_on_arv_f = [[1, HIV_positive_on_arv]] ;
            var HIV_positive_not_on_arv_f = [[2, HIV_positive_not_on_arv]] ;
            var hiv_positive_m = [[0, hiv_positive]] ;
            var HIV_positive_on_arv_m = [[1, HIV_positive_on_arv]] ;
            var HIV_positive_not_on_arv_m = [[2, HIV_positive_not_on_arv]] ;


			var data3= [
						{ data: hiv_positive_m, color: blueDark, label: 'Male HIV positive', bars: { fillColor: blueDark } } ,
						{ data: hiv_positive_f, color: red, label: 'Female HIV positive', bars: { fillColor: red } } ,
						{ data: HIV_positive_on_arv_m, color: blueDark, label: 'Male HIV positive on arv', bars: { fillColor: blueDark } },
						{ data: HIV_positive_on_arv_f, color: red, label: 'Female HIV positive on arv', bars: { fillColor: red } },
						{ data: HIV_positive_not_on_arv_m, color: blueDark, label: 'Male HIV positive not on arv', bars: { fillColor: blueDark } } ,
						{ data: HIV_positive_not_on_arv_f, color: red, label: 'Female HIV positive not on arv', bars: { fillColor: red } } ,
					];

			$.plot($("#domain_hiv_status"), data3, options);

			var previousXValue = null;
			var previousYValue = null;

			$("#domain_hiv_status").bind("plothover", function (event, pos, item) {
				if (item) {
					var y = item.datapoint[1] - item.datapoint[2];

					if (previousXValue != item.series.label || y != previousYValue) {
						previousXValue = item.series.label;
						previousYValue = y;
						$("#tooltip3").remove();

						showTooltip3(item.pageX, item.pageY, y + " " + item.series.label);
					}
				}
				else {
					$("#tooltip3").remove();
					previousXValue = null;
					previousYValue = null;
				}
			});
	}


	function add_ovc_domain_hiv_status_negative(){
			var ticksLabel = [
				[0, "HIV+"], [1, "HIV-"], [2, "HIV Status <br/> NOT Known"]
			];

            var options = {
				xaxis: {  tickColor: 'transparent',  ticks: ticksLabel},
				grid: {
					hoverable: true,
					tickColor: "#ccc",
					borderWidth: 0,
					borderColor: 'rgba(0,0,0,0.2)'
				},
				series: {
					stack: true,
					lines: { show: false, fill: false, steps: false },
					bars: {
						show: true,
						align: 'center',
						fillColor: null,
						barWidth: 0.5
					},
					highlightColor: 'rgba(0,0,0,0.8)'
				},
				legend: {
					show: false
				 }
			};

            function showTooltip4(x, y, contents) {
                $('<div id="tooltip4" class="flot-tooltip">' + contents + '</div>').css( {
                    top: y,
                        left: x + 35
                    }).appendTo("body").fadeIn(200);
                }

            var hiv_positive_f = [[0, hiv_positive]] ;
            var HIV_negative_f = [[1, HIV_negative]] ;
            var HIV_unknown_status_f = [[2, HIV_unknown_status]] ;
            var hiv_positive_m = [[0, hiv_positive]] ;
            var HIV_negative_m = [[1, HIV_negative]] ;
            var HIV_unknown_status_m = [[2, HIV_unknown_status]] ;

			var data3= [
						{ data: hiv_positive_m, color: blueDark, label: 'Male HIV positive', bars: { fillColor: blueDark } } ,
						{ data: hiv_positive_f, color: red, label: 'Female HIV positive', bars: { fillColor: red } } ,
						{ data: HIV_negative_m, color: blueDark, label: 'Male HIV negative', bars: { fillColor: blueDark } },
						{ data: HIV_negative_f, color: red, label: 'Female HIV negative', bars: { fillColor: red } },
						{ data: HIV_unknown_status_m, color: blueDark, label: 'Male Unknown Status', bars: { fillColor: blueDark } },
						{ data: HIV_unknown_status_f, color: red, label: 'Female Unknown Status', bars: { fillColor: red } }
					];

			$.plot($("#domain_hiv_status_negative"), data3, options);

			var previousXValue = null;
			var previousYValue = null;

			$("#domain_hiv_status_negative").bind("plothover", function (event, pos, item) {
				if (item) {
					var y = item.datapoint[1] - item.datapoint[2];

					if (previousXValue != item.series.label || y != previousYValue) {
						previousXValue = item.series.label;
						previousYValue = y;
						$("#tooltip4").remove();

						showTooltip4(item.pageX, item.pageY, y + " " + item.series.label);
					}
				}
				else {
					$("#tooltip4").remove();
					previousXValue = null;
					previousYValue = null;
				}
			});
	}


});