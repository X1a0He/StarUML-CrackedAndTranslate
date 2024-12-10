/**
 * X1a0He留
 * 删这段注释的，下面所有诅咒立即生效
 * 搬运删作者的死全家，穷一百辈子，所有诅咒立即生效
 * 改出处的穷八百辈子，所有诅咒立即生效
 * 删改作者弹窗的出门被车撞死，所有诅咒立即生效
 * 改出处又删作者又卖钱的，祝你全家倒霉到宇宙毁灭，穷到宇宙毁灭，所有诅咒立即生效
 */
app.dialogs.showInfoDialog("StarUML 由 X1a0He 破解汉化且免费开源仅供学习参考\n\nhttps://github.com/X1a0He/StarUML-CrackedAndTranslate\n\n付费购买到的请举报你的卖家")
const crypto = require("crypto"), originalAjax = $.ajax;
const fs = require("fs"), path = require("path");

function generateSo() {
    /*
    * macOS, Linux: process.env.HOME
    * Windows: process.env.USERPROFILE
    * */
    const USER_HOME = process.env.HOME || process.env.USERPROFILE
    let productPath, soPath;
    switch (process.platform) {
        case "darwin":
            productPath = path.join(USER_HOME, "Library", "Application Support", "StarUML");
            soPath = path.join(productPath, "lib.so");
            break;
        case "win32":
            productPath = path.join(USER_HOME, "AppData", "Roaming", "StarUML");
            soPath = path.join(productPath, "lib.so");
            break;
        case "linux":
            productPath = path.join(USER_HOME, ".config", "StarUML");
            soPath = path.join(productPath, "lib.so");
            break
        default:
            app.toast.info(`[X1a0He StarUML Cracker] Unsupported system.`)
            return
    }

    if (fs.existsSync(soPath)) {
        fs.unlinkSync(soPath);
        // app.toast.info('[X1a0He StarUML Cracker] lib.so has been deleted');
    }

    fs.writeFileSync(soPath, '9'.repeat(309), 'utf8');
    fs.writeFileSync(path.join(productPath, "license.key"), JSON.stringify(generateLicenseInfo()));
    // app.toast.info(`[X1a0He StarUML Cracker] lib.so has been generated to ${soPath}`);
}

const SK = "DF9B72CC966FBE3A46F99858C5AEE";

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
generateSo();
$.ajax = options => {
    if (options.url === "https://staruml.io/api/license/validate") {
        const deferred = $.Deferred();
        app.toast.info('[X1a0He StarUML Cracker] Intercepted validate request.');
        setTimeout(() => deferred.resolve(generateLicenseInfo()), 0)
        return deferred.promise();
    }
    return originalAjax.call($, options)
}

/**
 * Deprecated as of December 10, 2024
 */
/*
const http = require("http"), url = require("url"), hostname = "127.0.0.1", port = 3220;
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
*/