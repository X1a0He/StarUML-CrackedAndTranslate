const http = require("http"), url = require("url"), crypto = require("crypto"), originalPost = $.post;
const SK = "DF9B72CC966FBE3A46F99858C5AEE", hostname = "127.0.0.1", port = 3220;
$.post = (url, data, callback, dataType) => originalPost(url === "https://staruml.io/api/license/validate" ? "http://127.0.0.1:3220/api/license/validate" : url, data, callback, dataType);
const generateLicenseInfo = () => {
    const licenseInfo = { name: "Cracked by X1a0He", product: "STARUML.V6", licenseType: "PRO", quantity: "999", timestamp: `4102329600000`, crackedAuthor: "X1a0He", licenseKey: "" };
    licenseInfo.licenseKey = crypto.createHash("sha1").update(`${SK}${licenseInfo.name}${SK}${licenseInfo.product}-${licenseInfo.licenseType}${SK}${licenseInfo.quantity}${SK}${licenseInfo.timestamp}${SK}`).digest("hex").toUpperCase();
    return licenseInfo;
};
const server = http.createServer((req, res) => {
    const { pathname } = url.parse(req.url, true);
    if (pathname === "/api/license/validate") {
        res.setHeader("Content-Type", "application/json; charset=utf-8");
        res.statusCode = 200;
        res.end(JSON.stringify(generateLicenseInfo()));
        console.log(`validate hook By X1a0He StarUML Crack Server`);
    }
});
server.listen(port, hostname, () => console.log(`X1a0He StarUML Crack Server is running`));
