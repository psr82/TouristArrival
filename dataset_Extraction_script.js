const api = require("google-trends-api");
const fs = require("fs");

const geos = [
	"GB",	"RU",	"DE",	"UA",	"FI",	"FR",	"CH",	"SE",
	"US",	"AU",	"ZA",	"BR",	"IT",	"CA",	"JP",];
const categories = [
    categories= 'all',
];

const keywords = [
	"goa beach",    "goa flight",    "goa india",    "goa places", "goa hotel",	// "goa church" // "goa casino",	// "goa international airport",	// "goa watersports",	// "goa termperature",	// "goa night life",    // "goa sight seeing",
];

const startTime = new Date("February 21, 2012");
const endTime = new Date("June 03, 2020");

function createCSV(data, keyword, geo, category) {
	let str = "keywork;geo;category;date;value\n";
	for (let i = 0; i < data.length; i++) {
		const d = data[i];
		str = `${str}${keyword};${geo};${category};${d['formattedAxisTime']};${d['value'][0]}\n`;
	}

	fs.writeFile(`data/${keyword}__${geo}__${category}.csv`, str, function (err) {
		if (err) { console.log(err); return; }
		console.log(`Saved ${keyword}__${geo}__${category}.csv`);
	});
}
geos.forEach(function (geo) {
	categories.forEach(function (category) {
		keywords.forEach(function (keyword) {
			api.interestOverTime({
				keyword: keyword,
				geo: geo,
				category: category,
				startTime: startTime,
				endTime: endTime,
			})
				.then(function (res) {
					const data = JSON.parse(res)['default']['timelineData'];
					if (!data.length) {
						return;
					}
					console.log(`Keyword: '${keyword}' Geo: '${geo}' Category: '${category}' => ${data.length}`);

					createCSV(data, keyword, geo, category);
				})
				.catch(function (err) {
					console.log(`Error finding data for ${keyword}-${geo}-${category}`);
				});
		});
	});
});