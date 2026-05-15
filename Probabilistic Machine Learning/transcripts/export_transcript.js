(function() {
    let captions = [];
    // Selects each caption block based on your uploaded source structure
    document.querySelectorAll('.event-tab-list .index-event').forEach(item => {
        let time = item.querySelector('.event-time')?.innerText.trim() || "";
        let text = item.querySelector('.event-text span')?.innerText.trim() || "";
        if (text) {
            captions.push(`[${time}] ${text}`);
        }
    });
    
    if (captions.length === 0) {
        console.error("No captions found. Please make sure the 'Captions' tab is open on the page.");
        return;
    }

    // Creates and downloads a text file
    let blob = new Blob([captions.join('\n')], { type: 'text/plain' });
    let a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'panopto_transcript.txt';
    a.click();
    console.log("Exported " + captions.length + " caption lines.");
})();