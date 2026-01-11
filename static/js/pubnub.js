const pubnub = new PubNub({
    subscribeKey: "SECRET_KEY",
    uuid: "calweb-browser-" + Math.random().toString(36).slice(2)
});

const channel = "calweb-visual-state";

pubnub.addListener({
    message: function(event) {
        const mode = event.message.mode;
        if (mode === "day" || mode === "night") {
            document.body.classList.remove("day", "night");
            document.body.classList.add(mode);
        }
    }
});

pubnub.subscribe({
    channels: [channel]
});
