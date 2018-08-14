IR = {

};

// ex jQuery

jQuery.fn.toggleAttr = function(attr, v){
	if(v==undefined){
		v = attr;
	}
	thiz = this;
	if(thiz.attr(attr) == v){
		thiz.removeAttr(attr)
	}
	else{
		thiz.attr(attr,v);
	}
}


Date.prototype.format = function(format) {
	var o = {
		"M+": this.getMonth() + 1, //month 
		"d+": this.getDate(), //day 
		"h+": this.getHours(), //hour 
		"m+": this.getMinutes(), //minute 
		"s+": this.getSeconds(), //second 
		"q+": Math.floor((this.getMonth() + 3) / 3), //quarter 
		"S": this.getMilliseconds() //millisecond 
	};

	if (/(y+)/.test(format)) {
		format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
	}

	for (var k in o) {
		if (new RegExp("(" + k + ")").test(format)) {
			format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length));
		}
	}
	return format;
};

if(!Array.prototype.indexOfEx){
	Array.prototype.indexOfEx = function(obj, equ){
		var fn = typeof(equ) == "function" ? equ: function (v1,v2){
			return equ?v1[equ] == v2[equ]: v1.id == v2.id;
		};
		for (var i = 0; i < this.length; i++) {
			if(this[i]==obj || (typeof(this[i]) == "object" && typeof(obj) == "object" && fn(this[i], obj))) {
				return i;
			}
		};
		return -1;
	}
}

if(!Array.prototype.removeAt){
	Array.prototype.removeAt = function(index){
		return this.splice(index,1);
	}
}

if(!String.prototype.startsWith){
	String.prototype.startsWith = function(s){
		return this.indexOf(s)==0;
	};
}

+ function(B, $) {
	B.log = function(log) {
		console.log(log);
	};
	// B.msg = function(msg) {
	// 	B.log(msg);
	// };
	B.defdata = function(defdata, newdata) {
		for (var k in newdata) {
			if (typeof(defdata[k]) != "undefine") {
				defdata[k] = newdata[k];
			}
		}
		return defdata;
	};
	B.renderstr = function(tpl, data) {
		var str = tpl;
		for (k in data) {
			var v = data[k];
			var tk = "{" + k + "}";
			if (str.indexOf(tk) >= 0) {
				str = str.replace(new RegExp(tk, "gm"), v);
			}
		}
		return str;
	};
	B.back = function() {
		history.go(-1);
	};

	B.getValueByKey = function(s, k) {
		var reg = new RegExp("([\\?#]|^|&)" + k + "=([^&]*)(&|$)");
		var r = s.match(reg);
		if (r != null) return decodeURIComponent(r[2]);
		return null;
	}

	B.getQueryString = function(name) {
		return B.getValueByKey(window.location.search, name);
	}

	B.buildParam = function(raw, par, par_value) {
		var r = new RegExp('([&\?])'+par + '=[^&]*');
		var replaceText = par + '=' + par_value;
		var rs = raw.match(r);
		if (rs) {
			return raw.replace(r, rs[1] + replaceText);
		} else {
			if (raw.match('[\?]')) {
				return raw + '&' + replaceText;
			} else {
				return raw + '?' + replaceText;
			}
		}
		return raw + '\n' + par + '\n' + par_value;
	}
	B.reloadURL = function(){
		if(arguments.length>=2){
			var search = window.location.search;
			for (var i = 0; i < (arguments.length-1);  i+=2) {
				var k = arguments[i];
				var v = arguments[i+1];
				search = B.buildParam(search, k, v);
			};

			window.location.href = window.location.origin+window.location.pathname+search+window.location.hash;
		}
		else
			window.location.reload();
	};

	B.getInputValues = function(inps){
		var data = {};
		$.each(inps, function(index, val) {
			var thiz = $(val);
			data[thiz.attr('name')] = thiz.val();
		});
		return data;
	};

	B.verifyInputValues = function(inps){
		for (var i = 0; i < inps.length; i++) {
			var thiz = $(inps[i]);
			var val = thiz.val();
			if(thiz.attr('nullmsg') && !val){
				B.msg(thiz.attr('nullmsg'),function(){
					thiz.focus();
				});
				return false;
			}
		};
		return true;
	};

	B.timestamp = function(){
		return (new Date()).getTime();
	};

	B.smallImage = function(url){
		if(url && url.length>0){
			return B.buildParam(url, 'type', 'small');
		}
		else{
			return url;
		}
	};

	B.getSearchKeyValues = function(search){
		if(!search)
			search = window.location.search;
		var rt = /([^\?^\=^\&]+)=([^\?^\=^\&]+)/g;
		var rl = /([^\?^\=^\&]+)=([^\?^\=^\&]+)/;
		var res = {};

		var rs = search.match(rt);
		for (var i = 0; rs && i < rs.length; i++) {
			var ss = rs[i].match(rl);
			if(ss.length==3){
				res[ss[1]] = decodeURIComponent(ss[2]);
			}
		};
		return res;
	};

}(IR, jQuery);
