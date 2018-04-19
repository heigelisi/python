// ng-app
var app = angular.module('portalApp', ["ui.bootstrap", "ngAnimate", "slotGame", "lobbyNav"]);

/// 中奖名单
app.controller('WinnerListCtrl', ['$scope',
    function ($scope) {
        var list = [
            { "user": "jj***406", "money": 160025.24, "game": "MW电子" },
            { "user": "aaa***333", "money": 229058.74, "game": "MG电子" },
            { "user": "mma***369", "money": 195134.48, "game": "PT电子" },
            { "user": "a2***013", "money": 115493.58, "game": "BBIN电子" },
            { "user": "zho***33", "money": 142301.41, "game": "AG电子" },
            { "user": "jcj***123", "money": 292916.59, "game": "SG电子" },
            { "user": "aan***702", "money": 242220.92, "game": "PG电子" },
            { "user": "xi***499", "money": 254690.86, "game": "GPI电子" },
            { "user": "yj***977", "money": 104053.17, "game": "GNS电子" },
            { "user": "arh***77", "money": 250827.13, "game": "PP电子" },
            { "user": "aan***70", "money": 238539.33, "game": "HB电子" },
            { "user": "aa9***77", "money": 241416.61, "game": "JDB电子" },
            { "user": "yan***23", "money": 16056.71, "game": "CQ9电子" },
            { "user": "a16***713", "money": 170452.97, "game": "RT电子" },
            { "user": "jj2***00", "money": 112372.99, "game": "GA电子" },
            { "user": "my***717", "money": 133324.93, "game": "NE电子" },
            { "user": "zj***21", "money": 116641.73, "game": "BBIN电子" },
            { "user": "aj2***349", "money": 218806.91, "game": "MW电子" },
            { "user": "biy***799", "money": 120855.02, "game": "SG电子" },
            { "user": "xi***7as", "money": 218046.58, "game": "PG电子" },
            { "user": "lan***21", "money": 242827.75, "game": "GPI电子" },
            { "user": "do***797", "money": 30063.79, "game": "GNS电子" },
            { "user": "c***1", "money": 13541.8, "game": "PP电子" },
            { "user": "zhi***an", "money": 213411.69, "game": "HB电子" },
            { "user": "js3***06", "money": 279860.36, "game": "JDB电子" },
            { "user": "a1***767", "money": 111201.6, "game": "CQ9电子" },
            { "user": "lc***779", "money": 155124.7, "game": "AG电子" },
            { "user": "ak1***777", "money": 121050.65, "game": "MG电子" },
            { "user": "ys1***167", "money": 203372.69, "game": "PT电子" },
            { "user": "hu***ang", "money": 177268.39, "game": "BBIN电子" },
            { "user": "bti***129", "money": 39664.07, "game": "MW电子" },
            { "user": "gz***77", "money": 171983.74, "game": "SG电子" },
            { "user": "lz***720", "money": 237711.67, "game": "PG电子" },
            { "user": "lzj***lzj", "money": 114689.48, "game": "GPI电子" },
            { "user": "li7***070", "money": 90579.81, "game": "GNS电子" },
            { "user": "gsb***77", "money": 256232.41, "game": "CQ9电子" },
            { "user": "a97***97", "money": 123702.79, "game": "RT电子" },
            { "user": "a77***77", "money": 256935.33, "game": "GA电子" },
            { "user": "xi***n33", "money": 41261.92, "game": "NE电子" },
            { "user": "ji***011", "money": 97405.36, "game": "BBIN电子" },
            { "user": "M***4", "money": 271069.66, "game": "MW电子" },
            { "user": "dl1***764", "money": 81607.24, "game": "SG电子" },
            { "user": "aoi***ii", "money": 53485.61, "game": "PG电子" },
            { "user": "lx***xlx", "money": 275964.81, "game": "GPI电子" },
            { "user": "zha***99", "money": 12706.84, "game": "GNS电子" },
            { "user": "ljy***197", "money": 54556.44, "game": "PP电子" },
            { "user": "yan***jun", "money": 70929.39, "game": "CQ9电子" },
            { "user": "a29***96", "money": 36939.5, "game": "AG电子" },
            { "user": "oo1***420", "money": 40283.46, "game": "MG电子" },
            { "user": "lhc***12", "money": 220436.63, "game": "PT电子" }
        ];

        $scope.winnerList = [];

        for (var i = 0; i < 50; i++) {
            $scope.winnerList.push(list[i]);
        }
    }]);


$(document).ready(function () {
    //跑馬燈外掛  參考：http://aamirafridi.com/jquery/jquery-marquee-plugin
    //使用class 供應其他頁面不同跑馬燈需要時可以使用
    //如果同時不同頁面需要其他效果，請建新的
    //最新消息使用
    $('.marqueen').marquee({
        //speed in milliseconds of the marquee
        duration: 12500,
        //gap in pixels between the tickers
        gap: 50,
        //time in milliseconds before the marquee will start animating
        delayBeforeStart: 0,
        //'left' or 'right' or 'up' or 'right'
        direction: 'left',
        //true or false - should the marquee be duplicated to show an effect of continues flow
        duplicated: false,
        //hover over marquee to pause
        pauseOnHover: true
    });

    $('#language').hover(function () {
        $(this).children('#select-language').stop().slideToggle('fast');
    });

    $('nav > ul > li').hover(
        function () {
            $(this).children('.subnav').stop(true, true).slideDown('fast');
        },
        function () {
            $(this).children('.subnav').stop(true, true).slideUp('fast');
        });

    /// 2016/9/6 站长特殊需求：首页和电子页的超级彩金要同步
    /// 做法同SuperJackpot只是把 6 开头换成 6358

    function formatMoney(s, type) {
        s = (Math.round(s * 100) / 100).toString().replace(/^(\d*)$/, "$1.");
        s = (s + "00").replace(/(\d*\.\d{2})\d*/, "$1");
        s = s.replace(".", ",");
        var re = /(\d)(\d{3},)/;

        while (re.test(s)) {
            s = s.replace(re, "$1,$2");
        }

        s = s.replace(/,(\d{2})$/, ".$1");

        return s;
    };

    //準備起始值
    var start = parseInt('6358' + Math.floor(Math.random() * 1000));

    $("#super-jackpot").html(formatMoney(start));

    //Math.random() * 10 * 1000 秒後再加上一個亂數
    setInterval(function () {
        //取1~1000間的亂數 +1表示無條捨去小數點進位
        var add = (Math.random() * 1000);
        start += add;
        $("#super-jackpot").html(formatMoney(start));

    }, Math.random() * 2 * 10 * 1000);  //會隨機傳回0~1之間的浮點數，但並不包含1 * 10秒
});