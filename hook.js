const http = require("http"), url = require("url"), crypto = require("crypto"), originalPost = $.post;
const fs = require("fs"), path = require("path");

function generateSo() {
    /*
    * macOS, Linux: process.env.HOME
    * Windows: process.env.USERPROFILE
    * */
    const USER_HOME = process.env.HOME || process.env.USERPROFILE
    let soPath = path.join(USER_HOME, "Library", "Application Support", "StarUML", "lib.so");
    if (fs.existsSync(soPath)) {
        fs.unlinkSync(soPath);
        console.log(`[X1a0He StarUML Cracker] lib.so has been deleted`)
    }
    fs.writeFileSync(soPath, '9'.repeat(309), 'utf8');
    console.log(`[X1a0He StarUML Cracker] lib.so has been generated to ${USER_HOME}/Library/Application Support/StarUML/lib.so`)
}

const SK = "DF9B72CC966FBE3A46F99858C5AEE", hostname = "127.0.0.1", port = 3220;
$.post = (url, data, callback, dataType) => originalPost(url === "https://staruml.io/api/license/validate" ? "http://127.0.0.1:3220/api/license/validate" : url, data, callback, dataType);
const generateLicenseInfo = () => {
    const licenseInfo = {
        name: "GitHub: X1a0He/StarUML-CrackedAndTranslate",
        product: "STARUML.V6",
        licenseType: "PRO",
        quantity: "Unlimited",
        timestamp: `8640000000000000`,
        crackedAuthor: "X1a0He",
        licenseKey: ""
    };
    licenseInfo.licenseKey = crypto.createHash("sha1").update(`${SK}${licenseInfo.name}${SK}${licenseInfo.product}-${licenseInfo.licenseType}${SK}${licenseInfo.quantity}${SK}${licenseInfo.timestamp}${SK}`).digest("hex").toUpperCase();
    return licenseInfo;
};
const server = http.createServer((req, res) => {
    const {pathname} = url.parse(req.url, true);
    if (pathname === "/api/license/validate") {
        res.setHeader("Content-Type", "application/json; charset=utf-8");
        res.statusCode = 200;
        res.end(JSON.stringify(generateLicenseInfo()));
        console.log(`[X1a0He StarUML Cracker] Validate hooked by X1a0He StarUML Crack Server`);
    }
});
server.listen(port, hostname, () => console.log(`[X1a0He StarUML Cracker] Server is running`));
generateSo();