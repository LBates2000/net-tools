var page = require('webpage').create(),
    system = require('system'),
    timestamp, address, screenshot;

if (system.args.length === 1) {
    console.log('Usage: screenshot.js <address>');
    phantom.exit(1);
} else {
    address = system.args[1];
    screenshot = system.args[2];
};

page.settings.resourceTimeout = 5000 // wait 5 seconds for a response

page.viewportSize = {
    width: 1920,
    height: 1080
};

page.zoomFactor = 1;

page.onConsoleMessage = function(msg, lineNum, sourceId) {
    console.log('CONSOLE: ' + msg + ' (from line #' + lineNum + ' in "' + sourceId + '")');
};

page.onError = function(msg, trace) {
    var msgStack = ['ERROR: ' + msg];
    if (trace && trace.length) {
        msgStack.push('TRACE:');
        trace.forEach(function(t) {
            msgStack.push(' -> ' + t.file + ': ' + t.line + (t.function ? ' (in function "' + t.function+'")' : ''));
        });
    }

    console.error(msgStack.join('\n'));
};

page.onResourceError = function(resourceError) {
    console.log('Unable to load resource (#' + resourceError.id + ' address:' + resourceError.address + ')');
    console.log('Error code: ' + resourceError.errorCode + '. Description: ' + resourceError.errorString);
};

page.onResourceRequested = function(req) {
    console.log("onResourceRequested");
}

page.onResourceTimeout = function(request) {
    console.log('Response Timeout (#' + request.id + '): ' + JSON.stringify(request));
};

page.open(address, function(status) {
    if (status !== 'success') {
        console.log('Unable to load the address!');
        phantom.exit(1);
    } else {
        window.setTimeout(function() {
            page.render(screenshot);
            phantom.exit();
        }, 7500); // Wait for page to load
    }
});
