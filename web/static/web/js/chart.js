Highcharts.chart('hourly', {

    title: {
        text: 'Популярное время размещения'
    },

    yAxis: {
        title: {
            text: 'Количество объявлений'
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        series: {
            pointStart: 0
        }
    },

    series: [{
        name: 'Популярное время размещения',
        data: hourly
    }],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }
});

Highcharts.chart('weekly', {

    title: {
        text: 'Популярный день недели'
    },

    yAxis: {
        title: {
            text: 'Количество объявлений'
        }
    },

    xAxis: {
        categories: [
            'Понедельник',
            'Вторник',
            'Среда',
            'Четверг',
            'Пятница',
            'Суббота',
            'Воскресенье'
        ],

        tickInterval: 1
    },

    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        series: {
            pointStart: 0
        }
    },

    series: [{
        name: 'Популярный день недели',
        data: weekly
    }],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }
});