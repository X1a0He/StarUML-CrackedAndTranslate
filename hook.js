/**
 * X1a0He留
 * 删这段注释的，下面所有诅咒立即生效
 * 搬运删作者的死全家，穷一百辈子，所有诅咒立即生效
 * 改出处的穷八百辈子，所有诅咒立即生效
 * 删改作者弹窗的出门被车撞死，所有诅咒立即生效
 * 改出处又删作者又卖钱的，祝你全家倒霉到宇宙毁灭，穷到宇宙毁灭，所有诅咒立即生效
 */
let crypto;
const fs = require("fs"), path = require("path");
let originalAjax, originalFetch;

function getProductPath() {
    const USER_HOME = process.env.HOME || process.env.USERPROFILE;
    switch (process.platform) {
        case "darwin":
            return path.join(USER_HOME, "Library", "Application Support", "StarUML");
        case "win32":
            return path.join(USER_HOME, "AppData", "Roaming", "StarUML");
        case "linux":
            return path.join(USER_HOME, ".config", "StarUML");
        default:
            // app.toast.info(`[X1a0He StarUML Cracker] Unsupported system.`);
            return null;
    }
}

function generateSo() {
    const soPath = path.join(getProductPath(), "lib.so");
    if (fs.existsSync(soPath)) {
        fs.unlinkSync(soPath);
        // app.toast.info('[X1a0He StarUML Cracker] lib.so has been deleted');
    }

    fs.writeFileSync(soPath, "9".repeat(309), "utf8");
    // app.toast.info(`[X1a0He StarUML Cracker] lib.so has been generated to ${soPath}`);
}

/**
 * StarUML v6
 * */
function CrackV6() {
    originalAjax = $.ajax;

    const SK = "DF9B72CC966FBE3A46F99858C5AEE";

    const generateLicenseInfo = () => {
        const crackAuthor = "GitHub: X1a0He/StarUML-CrackedAndTranslate"
        const licenseInfo = {
            name: crackAuthor,
            product: "STARUML.V6",
            licenseType: "PRO",
            quantity: crackAuthor,
            timestamp: `8640000000000000`,
            crackedAuthor: crackAuthor,
            licenseKey: "",
        };
        licenseInfo.licenseKey = crypto
            .createHash("sha1")
            .update(
                `${ SK }${ licenseInfo.name }${ SK }${ licenseInfo.product }-${ licenseInfo.licenseType }${ SK }${ licenseInfo.quantity }${ SK }${ licenseInfo.timestamp }${ SK }`
            )
            .digest("hex")
            .toUpperCase();
        return licenseInfo;
    };

    fs.writeFileSync(
        path.join(getProductPath(), "license.key"),
        JSON.stringify(generateLicenseInfo())
    );

    $.ajax = (options) => {
        if (options.url === "https://staruml.io/api/license/validate") {
            const deferred = $.Deferred();
            app.toast.info("[X1a0He StarUML Cracker] Intercepted validate request.");
            setTimeout(() => deferred.resolve(generateLicenseInfo()), 0);
            return deferred.promise();
        }
        return originalAjax.call($, options);
    };
}

/**
 * StarUML v7
 * */
function base64ToArrayBuffer(base64) {
    const binary = atob(base64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
    }
    return bytes;
}

async function importAESKey(base64Key) {
    const keyBuffer = base64ToArrayBuffer(base64Key);
    return crypto.subtle.importKey(
        'raw',
        keyBuffer,
        { name: 'AES-GCM' },
        true,
        ['encrypt', 'decrypt'],
    );
}

async function encryptString(plainText, key) {
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const encodedPlainText = new TextEncoder().encode(plainText);
    const encrypted = await crypto.subtle.encrypt(
        {
            name: 'AES-GCM',
            iv: iv,
        },
        key,
        encodedPlainText,
    );
    const ivBase64 = btoa(String.fromCharCode(...iv));
    const encryptedBase64 = btoa(String.fromCharCode(...new Uint8Array(encrypted)));
    return `${ ivBase64 }:${ encryptedBase64 }`;
}

async function CrackV7(key) {
    const { machineId } = require("node-machine-id");
    originalFetch = global.fetch;
    const LICENSE_SERVER_URL = "https://dev.staruml-io-astro.pages.dev/api/license-manager";
    const deviceId = await machineId();
    const licenseData = {
        name: 'GitHub: X1a0He/StarUML-CrackedAndTranslate',
        product: 'STARUML.V7',
        edition: 'CO',
        deviceId: deviceId,
        licenseKey: '',
    };
    const activation_code = await encryptString(JSON.stringify(licenseData), key)
    fs.writeFileSync(
        path.join(getProductPath(), "activation.key"),
        activation_code
    );
    global.fetch = async function (...args) {
        const [input] = args;
        if (input === `${ LICENSE_SERVER_URL }/activate`) {
            return new Response(
                JSON.stringify({ success: true, activation_code, }), {
                    status: 200,
                    headers: { 'Content-Type': 'application/json' }
                }
            )
        }

        if (input === `${ LICENSE_SERVER_URL }/validate`) {
            const validation_code = await encryptString(deviceId, key);
            return new Response(
                JSON.stringify({ success: true, validation_code, }), {
                    status: 200,
                    headers: { 'Content-Type': 'application/json' }
                }
            )
        }
        return originalFetch.apply(this, args);
    };
}

async function main() {
    generateSo();
    const pkg = require('../package.json');

    switch (pkg.productId || pkg.config.product_id) {
        case "STARUML.V6":
            crypto = require('crypto');
            CrackV6();
            break;
        case "STARUML.V7":
            crypto = globalThis.crypto;
            await CrackV7(await importAESKey('y0JMc9mvB1uvIi82GhdMJQXzVJxl+1Lc0RqZqWaQvx0='));
    }
}

(async () => {
    await main();
})();
