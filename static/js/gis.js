var cpimsCategory = {};

cpimsCategory['CDIS'] = 'Abandoned';
cpimsCategory['CDSA'] = 'Abduction';
cpimsCategory['CLAB'] = 'Child Affected by HIV/AIDS';
cpimsCategory['CORP'] = 'Child Delinquency';
cpimsCategory['COSR'] = 'Child headed household';
cpimsCategory['CTRF'] = 'Child Labour';
cpimsCategory['CCCM'] = 'Child Marriage';
cpimsCategory['SCCI'] = 'Child of imprisoned parent (s)';
cpimsCategory['CSAB'] = 'Child offender';
cpimsCategory['CSAD'] = 'Child out of school';
cpimsCategory['CSHV'] = 'Child pregnancy';
cpimsCategory['CSDQ'] = 'Child radicalization';
cpimsCategory['CCCT'] = 'Child truancy';
cpimsCategory['CSCL'] = 'Child with disability';
cpimsCategory['CCIP'] = 'Children on the streets';
cpimsCategory['CCCP'] = 'Custody';
cpimsCategory['CCDF'] = 'Defilement';
cpimsCategory['CSCT'] = 'Disputed paternity';
cpimsCategory['CSDS'] = 'Drug and Substance Abuse';
cpimsCategory['CCEA'] = 'Emotional Abuse';
cpimsCategory['CSCS'] = 'FGM';
cpimsCategory['CSCU'] = 'Harmful cultural practice';
cpimsCategory['CSDF'] = 'Incest';
cpimsCategory['CSDP'] = 'Inheritance/Succession';
cpimsCategory['CFGM'] = 'Internally displaced child';
cpimsCategory['CHCP'] = 'Lost and found children';
cpimsCategory['CSIC'] = 'Neglect';
cpimsCategory['CIDC'] = 'Orphaned Child';
cpimsCategory['CLFC'] = 'Parental child abduction';
cpimsCategory['CSNG'] = 'Physical abuse/violence';
cpimsCategory['CPCA'] = 'Refugee Children';
cpimsCategory['CPAV'] = 'Registration';
cpimsCategory['CSRC'] = 'Sexual assault';
cpimsCategory['CSRG'] = 'Sexual Exploitation and abuse';
cpimsCategory['CSSA'] = 'Sick Child (Chronic Illness)';
cpimsCategory['CSSO'] = 'Sodomy';
cpimsCategory['CSTC'] = 'Trafficked child';
cpimsCategory['CSUC'] = 'Unlawful confinement';

//All colors
var dataColors = {};
//Reds
dataColors[1] = {};
dataColors[1][8] = ['#fff7ec', '#fee8c8', '#fdd49e', '#fdbb84', '#fc8d59', '#ef6548', '#d7301f', '#990000'];
dataColors[1][7] = ['#fef0d9', '#fdd49e', '#fdbb84', '#fc8d59', '#ef6548', '#d7301f', '#990000'];
dataColors[1][6] = ['#fef0d9', '#fdd49e', '#fdbb84', '#fc8d59', '#e34a33', '#b30000'];
dataColors[1][5] = ['#fef0d9', '#fdcc8a', '#fc8d59', '#e34a33', '#b30000'];
dataColors[1][4] = ['#fef0d9', '#fdcc8a', '#fc8d59', '#d7301f'];
//Blues
dataColors[2] = {};
dataColors[2][8] = ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#084594'];
dataColors[2][7] = ['#eff3ff', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#084594'];
dataColors[2][6] = ['#eff3ff', '#c6dbef', '#9ecae1', '#6baed6', '#3182bd', '#08519c'];
dataColors[2][5] = ['#eff3ff', '#bdd7e7', '#6baed6', '#3182bd', '#08519c'];
dataColors[2][4] = ['#eff3ff', '#bdd7e7', '#6baed6', '#2171b5'];
//Purples
dataColors[3] = {};
dataColors[3][8] = ['#fcfbfd', '#efedf5', '#dadaeb', '#bcbddc', '#9e9ac8', '#807dba', '#6a51a3', '#4a1486'];
dataColors[3][7] = ['#f2f0f7', '#dadaeb', '#bcbddc', '#9e9ac8', '#807dba', '#6a51a3', '#4a1486'];
dataColors[3][6] = ['#f2f0f7', '#dadaeb', '#bcbddc', '#9e9ac8', '#756bb1', '#54278f'];
dataColors[3][5] = ['#f2f0f7', '#cbc9e2', '#9e9ac8', '#756bb1', '#54278f'];
dataColors[3][4] = ['#f2f0f7', '#cbc9e2', '#9e9ac8', '#6a51a3'];
//Greens
dataColors[4] = {};
dataColors[4][8] = ['#f7fcf5', '#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#005a32'];
dataColors[4][7] = ['#edf8e9', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#005a32'];
dataColors[4][6] = ['#edf8e9', '#c7e9c0', '#a1d99b', '#74c476', '#31a354', '#006d2c'];
dataColors[4][5] = ['#edf8e9', '#bae4b3', '#74c476', '#31a354', '#006d2c'];
dataColors[4][4] = ['#edf8fb', '#b2e2e2', '#66c2a4', '#238b4'];
//RedBlues
dataColors[5] = {};
dataColors[5][8] = ['#d73027', '#f46d43', '#fdae61', '#fee090', '#e0f3f8', '#abd9e9', '#74add1', '#4575b4'];
dataColors[5][7] = ['#d73027', '#fc8d59', '#fee090', '#ffffbf', '#e0f3f8', '#91bfdb', '#4575b4'];
dataColors[5][6] = ['#d73027', '#fc8d59', '#fee090', '#e0f3f8', '#91bfdb', '#4575b4'];
dataColors[5][5] = ['#d7191c', '#fdae61', '#ffffbf', '#abd9e9', '#2c7bb6'];
dataColors[5][4] = ['#d7191c', '#fdae61', '#abd9e9', '#2c7bb6'];
//RedGreen
dataColors[6] = {};
dataColors[6][8] = ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850'];
dataColors[6][7] = ['#d73027', '#fc8d59', '#fee08b', '#ffffbf', '#d9ef8b', '#91cf60', '#1a9850'];
dataColors[6][6] = ['#d73027', '#fc8d59', '#fee08b', '#d9ef8b', '#91cf60', '#1a9850'];
dataColors[6][5] = ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641'];
dataColors[6][4] = ['#d7191c', '#fdae61', '#a6d96a', '#1a9641'];
//RedBrown
dataColors[7] = {};
dataColors[7][8] = ['#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#e0e0e0', '#bababa', '#878787', '#4d4d4d'];
dataColors[7][7] = ['#b2182b', '#ef8a62', '#fddbc7', '#ffffff', '#e0e0e0', '#999999', '#4d4d4d'];
dataColors[7][6] = ['#b2182b', '#ef8a62', '#fddbc7', '#e0e0e0', '#999999', '#4d4d4d'];
dataColors[7][5] = ['#ca0020', '#f4a582', '#ffffff', '#bababa', '#404040'];
dataColors[7][4] = ['#ca0020', '#f4a582', '#bababa', '#404040'];
//PurpleGreen
dataColors[8] = {};
dataColors[8][8] = ['#762a83', '#9970ab', '#c2a5cf', '#e7d4e8', '#d9f0d3', '#a6dba0', '#5aae61', '#1b7837'];
dataColors[8][7] = ['#762a83', '#af8dc3', '#e7d4e8', '#f7f7f7', '#d9f0d3', '#7fbf7b', '#1b7837'];
dataColors[8][6] = ['#762a83', '#af8dc3', '#e7d4e8', '#d9f0d3', '#7fbf7b', '#1b7837'];
dataColors[8][5] = ['#7b3294', '#c2a5cf', '#f7f7f7', '#a6dba0', '#008837'];
dataColors[8][4] = ['#7b3294', '#c2a5cf', '#a6dba0', '#008837'];

var handleVars  = function() {
    "use strict";
 
};

var handleDatepicker = function() {
    $('#start_date').datepicker({
        todayHighlight: true,
        autoclose: true
    });
    $('#end_date').datepicker({
        todayHighlight: true,
        autoclose: true
    });
};

var GIS = function () {
	"use strict";
	
	return {
		//main function
		init: function () {
		    // Initialize variables
			handleVars();
			handleDatepicker();
		}
    };
}();