/**
 * X1a0He留
 * 删这段注释的，下面所有诅咒立即生效
 * 搬运删作者的死全家，穷一百辈子，所有诅咒立即生效
 * 改出处的穷八百辈子，所有诅咒立即生效
 * 删改作者弹窗的出门被车撞死，所有诅咒立即生效
 * 改出处又删作者又卖钱的，祝你全家倒霉到宇宙毁灭，穷到宇宙毁灭，所有诅咒立即生效
 */
const crypto = globalThis.crypto;
const fs = require("fs"), path = require("path");
const { app } = require("electron");

function getProductPath() {
    return app.getPath("userData");
}

function generateSo() {
    const soPath = path.join(getProductPath(), "lib.so");
    fs.writeFileSync(soPath, "9".repeat(309), "utf8");
    // app.toast.info(`[X1a0He StarUML Cracker] lib.so has been generated to ${soPath}`);
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
    const originalFetch = global.fetch;
    const LICENSE_SERVER_URL = "https://staruml.io/api/license-manager";
    const deviceId = await machineId();
    const licenseData = {
        name: 'GitHub: X1a0He/StarUML-CrackedAndTranslate',
        product: 'STARUML.V7',
        edition: 'PRO',
        deviceId: deviceId,
        licenseKey: '',
    };
    const activation_code = await encryptString(JSON.stringify(licenseData), key)
    fs.writeFileSync(
        path.join(getProductPath(), "activation.key"),
        activation_code
    );
    global.fetch = async function (...args) {
        const [input, options] = args;
        if (input === `${ LICENSE_SERVER_URL }/activate`) {
            const { license_key: licenseKey } = JSON.parse(options.body);
            const activation_code = await encryptString(
                JSON.stringify({ ...licenseData, licenseKey }), key
            );
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
    const pkg = require('../package.json');
    if ((pkg.productId || pkg.config?.product_id) !== "STARUML.V7") {
        throw new Error("仅支持 StarUML v7");
    }

    generateSo();
    await CrackV7(await importAESKey('y0JMc9mvB1uvIi82GhdMJQXzVJxl+1Lc0RqZqWaQvx0='));
}

module.exports = main();
