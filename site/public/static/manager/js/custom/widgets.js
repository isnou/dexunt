"use strict";

// Class definition
var KTWidgets = function () {
    // Chart widgets based on Apexcharts. For more info check the official documentation:  https://apexcharts.com/
    
    var initChartsWidget1 = function(tab, selector, data, dates, initByDefault) {
        var chart = {
            self: null,
            rendered: false
        };

        var tab = document.querySelector(tab);

        var initChart = function() {
            var element = document.querySelector(selector);
            var height = parseInt(KTUtil.css(element, 'height'));
            var labelColor = KTUtil.getCssVariableValue('--bs-gray-500');
            var borderColor = KTUtil.getCssVariableValue('--bs-gray-200');
            var baseColor = KTUtil.getCssVariableValue('--bs-success');
            var lightColor = KTUtil.getCssVariableValue('--bs-light');

            if (!element) {
                return;
            }

            var options = {
                series: [{
                    name: 'Net Profit',
                    data: data
                }],
                chart: {
                    fontFamily: 'inherit',
                    type: 'area',
                    height: 350,
                    toolbar: {
                        show: false
                    }
                },
                plotOptions: {

                },
                legend: {
                    show: false
                },
                dataLabels: {
                    enabled: false
                },
                fill: {
                    type: 'solid',
                    opacity: 1
                },
                stroke: {
                    curve: 'smooth',
                    show: true,
                    width: 3,
                    colors: [baseColor]
                },
                xaxis: {
                    categories: dates,
                    axisBorder: {
                        show: false,
                    },
                    axisTicks: {
                        show: false
                    },
                    labels: {
                        style: {
                            colors: labelColor,
                            fontSize: '12px'                         
                        }
                    },
                    crosshairs: {
                        position: 'front',
                        stroke: {
                            color: baseColor,
                            width: 1,
                            dashArray: 3
                        }
                    },
                    tooltip: {
                        enabled: true,
                        formatter: undefined,
                        offsetY: 0,
                        style: {
                            fontSize: '12px'
                        }
                    }
                },
                yaxis: {
                    labels: {
                        style: {
                            colors: labelColor,
                            fontSize: '12px'
                        }
                    }
                },
                states: {
                    normal: {
                        filter: {
                            type: 'none',
                            value: 0
                        }
                    },
                    hover: {
                        filter: {
                            type: 'none',
                            value: 0
                        }
                    },
                    active: {
                        allowMultipleDataPointsSelection: false,
                        filter: {
                            type: 'none',
                            value: 0
                        }
                    }
                },
                tooltip: {
                    style: {
                        fontSize: '12px'
                    },
                    y: {
                        formatter: function (val) {
                            return "$" + val + " thousands"
                        }
                    }
                },
                colors: [lightColor],
                grid: {
                    borderColor: borderColor,
                    strokeDashArray: 4,
                    yaxis: {
                        lines: {
                            show: true
                        }
                    }
                },
                markers: {
                    strokeColor: baseColor,
                    strokeWidth: 3
                }
            };

            chart.self = new ApexCharts(element, options);
           
            // Set timeout to properly get the parent elements width
            setTimeout(function() {
                chart.self.render();
                chart.rendered = true;
            }, 100); 
        }

        if (initByDefault === true) {
            initChart();
        }

		tab.addEventListener('shown.bs.tab', function(event) {
			if (chart.rendered == false) {
                initChart();
			}
		});

        // Update chart on theme mode change
        KTThemeMode.on("kt.thememode.change", function() {                
            if (chart.rendered) {
                chart.self.destroy();
            }

            initChart();
        });
    }

    var initChartsWidget2 = function() {
        var element = document.getElementById("kt_charts_widget_2_chart");

        var height = parseInt(KTUtil.css(element, 'height'));
        var labelColor = KTUtil.getCssVariableValue('--bs-gray-500');
        var borderColor = KTUtil.getCssVariableValue('--bs-gray-200');
        var baseColor = KTUtil.getCssVariableValue('--bs-primary');
        var secondaryColor = KTUtil.getCssVariableValue('--bs-gray-300');

        if (!element) {
            return;
        }

        var options = {
            series: [{
                name: 'Net Profit',
                data: [44, 55, 57, 56, 61, 58]
            }, {
                name: 'Revenue',
                data: [76, 85, 101, 98, 87, 105]
            }],
            chart: {
                fontFamily: 'inherit',
                type: 'bar',
                height: height,
                toolbar: {
                    show: false
                }
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: ['30%'],
                    borderRadius: 4
                },
            },
            legend: {
                show: false
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                show: true,
                width: 2,
                colors: ['transparent']
            },
            xaxis: {
                categories: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                axisBorder: {
                    show: false,
                },
                axisTicks: {
                    show: false
                },
                labels: {
                    style: {
                        colors: labelColor,
                        fontSize: '12px'
                    }
                }
            },
            yaxis: {
                labels: {
                    style: {
                        colors: labelColor,
                        fontSize: '12px'
                    }
                }
            },
            fill: {
                opacity: 1
            },
            states: {
                normal: {
                    filter: {
                        type: 'none',
                        value: 0
                    }
                },
                hover: {
                    filter: {
                        type: 'none',
                        value: 0
                    }
                },
                active: {
                    allowMultipleDataPointsSelection: false,
                    filter: {
                        type: 'none',
                        value: 0
                    }
                }
            },
            tooltip: {
                style: {
                    fontSize: '12px'
                },
                y: {
                    formatter: function (val) {
                        return "$" + val + " thousands"
                    }
                }
            },
            colors: [baseColor, secondaryColor],
            grid: {
                borderColor: borderColor,
                strokeDashArray: 4,
                yaxis: {
                    lines: {
                        show: true
                    }
                }
            }
        };

        var chart = new ApexCharts(element, options);
        chart.render();      
    }
    
    // Public methods
    return {
        init: function () {            
            // Init widget chart 1 instances
            initChartsWidget1(
                '#kt_chart_widget_1_tab_1',
                '#kt_charts_widget_1_chart_1',
                [30, 30, 36, 36, 34, 34, 38, 38, 32, 32, 36, 36, 41, 41, 37, 37], 
                ['Jul 15', 'Aug 1', 'Agu 15', 'Sep 1', 'Sep 15', 'Oct 1', 'Oct 15', 'Nov 1', 'Nov 15', 'Dec 1', 'Dec 15', 'Jan 1', 'Jan 15', 'Feb 1', 'Feb 15', 'Mar 1'],
                true
            );
            
            initChartsWidget1(
                '#kt_chart_widget_1_tab_2',
                '#kt_charts_widget_1_chart_2',
                [40, 40, 30, 30, 34, 34, 45, 45, 35, 35, 25, 25, 30, 30, 47, 47], 
                ['Jul 15', 'Aug 1', 'Agu 15', 'Sep 1', 'Sep 15', 'Oct 1', 'Oct 15', 'Nov 1', 'Nov 15', 'Dec 1', 'Dec 15', 'Jan 1', 'Jan 15', 'Feb 1', 'Feb 15', 'Mar 1'],
                false
            );

            initChartsWidget1(
                '#kt_chart_widget_1_tab_3',
                '#kt_charts_widget_1_chart_3',
                [25, 25, 50, 50, 44, 44, 58, 58, 22, 22, 56, 56, 21, 21, 47, 47], 
                ['Jul 15', 'Aug 1', 'Agu 15', 'Sep 1', 'Sep 15', 'Oct 1', 'Oct 15', 'Nov 1', 'Nov 15', 'Dec 1', 'Dec 15', 'Jan 1', 'Jan 15', 'Feb 1', 'Feb 15', 'Mar 1'],
                false
            );

            initChartsWidget1(
                '#kt_chart_widget_1_tab_4',
                '#kt_charts_widget_1_chart_4',
                [30, 30, 26, 26, 44, 44, 38, 38, 52, 52, 26, 26, 61, 61, 37, 37], 
                ['Jul 15', 'Aug 1', 'Agu 15', 'Sep 1', 'Sep 15', 'Oct 1', 'Oct 15', 'Nov 1', 'Nov 15', 'Dec 1', 'Dec 15', 'Jan 1', 'Jan 15', 'Feb 1', 'Feb 15', 'Mar 1'],
                false
            );
             
            initChartsWidget2();
        }
    }
}();

// On document ready
KTUtil.onDOMContentLoaded(function() {
    KTWidgets.init();
});