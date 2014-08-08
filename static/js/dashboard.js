//DataTables
//Sort file size data.
jQuery.extend(jQuery.fn.dataTableExt.oSort, {
    "file-size-units": {
        K: 1024,
        M: Math.pow(1024, 2),
        G: Math.pow(1024, 3),
        T: Math.pow(1024, 4),
        P: Math.pow(1024, 5),
        E: Math.pow(1024, 6)
    },

    "file-size-pre": function (a) {
        var x = a.substring(0, a.length - 1);
        var x_unit = a.substring(a.length - 1, a.length);
        if (jQuery.fn.dataTableExt.oSort['file-size-units'][x_unit]) {
            return parseInt(x * jQuery.fn.dataTableExt.oSort['file-size-units'][x_unit], 10);
        }
        else {
            return parseInt(x + x_unit, 10);
        }
    },

    "file-size-asc": function (a, b) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "file-size-desc": function (a, b) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
});

//DataTables
//Sort numeric data which has a percent sign with it.
jQuery.extend(jQuery.fn.dataTableExt.oSort, {
    "percent-pre": function (a) {
        var x = (a === "-") ? 0 : a.replace(/%/, "");
        return parseFloat(x);
    },

    "percent-asc": function (a, b) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "percent-desc": function (a, b) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
});

//DataTables
//Sort IP addresses
jQuery.extend(jQuery.fn.dataTableExt.oSort, {
    "ip-address-pre": function (a) {
        // split the address into octets
        //
        var x = a.split('.');

        // pad each of the octets to three digits in length
        //
        function zeroPad(num, places) {
            var zero = places - num.toString().length + 1;
            return new Array(+(zero > 0 && zero)).join("0") + num;
        }

        // build the resulting IP
        var r = '';
        for (var i = 0; i < x.length; i++)
            r = r + zeroPad(x[i], 3);

        // return the formatted IP address
        //
        return r;
    },

    "ip-address-asc": function (a, b) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "ip-address-desc": function (a, b) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
});

// If dataTable with provided ID exists, destroy it.
function destroy_dataTable(table_id) {
    var table = $("#" + table_id);
    var ex = document.getElementById(table_id);
    if ($.fn.DataTable.fnIsDataTable(ex)) {
        table.hide().dataTable().fnClearTable();
        table.dataTable().fnDestroy();
    }
}

function get_os_data(url, element) {
    $.get(url, function (data) {
        $(element).text(data);
    }, "json");
}

var dashboard = {};

dashboard.getUptime = function () {
    get_os_data('/info/uptime/', "#get-uptime");
};

dashboard.getOSname = function () {
    get_os_data('/info/platform/osname/', "#get-osname");
};

dashboard.getHostname = function () {
    get_os_data('/info/platform/hostname/', "#get-hostname");
};

dashboard.getKernel = function () {
    get_os_data('/info/platform/kernel/', "#get-kernel");
};

dashboard.getCPUcount = function () {
    get_os_data('/info/getcpus/count/', "#get-cpucount");
};

dashboard.getCPUtype = function () {
    get_os_data('/info/getcpus/type/', "#get-cputype");
};

dashboard.getDisk = function () {
    $.getJSON('/info/getdisk/', function (data) {
        destroy_dataTable("get_disk");
        var $filterPs = $("#filter-ps");
        $filterPs.val("").off("keyup");
        var psTable = $("#get_disk").dataTable({
            aaData: data,
            aoColumns: [
                { sTitle: "FILESYSTEM" },
                { sTitle: "SIZE" },
                { sTitle: "USED" },
                { sTitle: "AVAIL" },
                { sTitle: "USE %" },
                { sTitle: "MOUNTED" }
            ],
            bPaginate: false,
            bFilter: true,
            sDom: "lrtip",
            bAutoWidth: false,
            bInfo: false
        }).fadeIn();
        $filterPs.on("keyup", function () {
            psTable.fnFilter(this.value);
        });
    });
};

dashboard.getUsers = function () {
    $.getJSON('/info/getusers/', function (data) {
        destroy_dataTable("get_users");
        var $filterPs = $("#filter-ps");
        $filterPs.val("").off("keyup");
        var psTable = $("#get_users").dataTable({
            aaData: data,
            aoColumns: [
                { sTitle: "USER" },
                { sTitle: "TTY" },
                { sTitle: "LOOGED IN FROM",
                    sDefaultContent: "unavailable" }
            ],
            aaSorting: [
                [0, "desc"]
            ],
            bPaginate: true,
            sPaginationType: "two_button",
            bFilter: false,
            bAutoWidth: false,
            bInfo: false
        }).fadeIn();
        $filterPs.on("keyup", function () {
            psTable.fnFilter(this.value);
        });
    });
};

dashboard.getNetstat = function () {
    $.getJSON('/info/getnetstat/', function (data) {
        destroy_dataTable("get_netstat");
        var $filterPs = $("#filter-ps");
        $filterPs.val("").off("keyup");
        var psTable = $("#get_netstat").dataTable({
            aaData: data,
            aoColumns: [
                { sTitle: "COUNT" },
                { sTitle: "LOCAL IP" },
                { sTitle: "LOCAL PORT" },
                { sTitle: "FOREIGN" }
            ],
            bPaginate: true,
            sPaginationType: "two_button",
            bFilter: true,
            sDom: "lrtip",
            bAutoWidth: false,
            bInfo: false
        }).fadeIn();
        $filterPs.on("keyup", function () {
            psTable.fnFilter(this.value);
        });
    });
};

dashboard.getProc = function () {
    $.getJSON('/info/proc/', function (data) {
        destroy_dataTable("get_proc");
        var $filterPs = $("#filter-ps");
        $filterPs.val("").off("keyup");
        var psTable = $("#get_proc").dataTable({
            aaData: data,
            aoColumns: [
                { sTitle: "USER" },
                { sTitle: "PID" },
                { sTitle: "%CPU" },
                { sTitle: "%MEM" },
                { sTitle: "VSZ" },
                { sTitle: "RSS" },
                { sTitle: "TTY" },
                { sTitle: "STAT" },
                { sTitle: "START" },
                { sTitle: "TIME" },
                { sTitle: "COMMAND" }
            ],
            bPaginate: true,
            sPaginationType: "full_numbers",
            bFilter: true,
            sDom: "lrtip",
            bAutoWidth: false,
            bInfo: false
        }).fadeIn();
        $filterPs.on("keyup", function () {
            psTable.fnFilter(this.value);
        });
    });
};

dashboard.getIps = function () {
    $.getJSON('/info/getips/', function (data) {
        destroy_dataTable("get_ips");
        var $filterPs = $("#filter-ps");
        $filterPs.val("").off("keyup");
        var psTable = $("#get_ips").dataTable({
            aaData: data,
            aoColumns: [
                { sTitle: "INTERFACE" },
                { sTitle: "MAC ADDRESS" },
                { sTitle: "IP ADDRESS" },
                { sTitle: "IP ADDRESS",
                    sDefaultContent: "unavailable" }
            ],
            bPaginate: false,
            bFilter: true,
            sDom: "lrtip",
            bAutoWidth: false,
            bInfo: false
        }).fadeIn();
        $filterPs.on("keyup", function () {
            psTable.fnFilter(this.value);
        });
    });
};

// Expand-Contract div/table
$(document).ready(function () {
    $(".widget-content").show();
    $(".widget-header").click(function () {
        $(this).next(".widget-content").slideToggle(500);
        $("i", this).toggleClass("icon-minus icon-plus");
    });
});
