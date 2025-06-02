document.addEventListener('DOMContentLoaded', function () {
    const essenceRunesContainer = document.getElementById('essence-runes-container');
    const incantationRunesContainer = document.getElementById('incantation-runes-container');
    const availableSomaticList = document.getElementById('available-somatic-runes');
    const finalRuneOrderListUl = document.getElementById('final-rune-order');
    const spellForm = document.getElementById('spell-form');
    const spellNameInput = document.getElementById('spell-name');
    const spellDescriptionInput = document.getElementById('spell-description');
    const createSpellButton = document.getElementById('create-spell-button');
    const saveSpellButton = document.getElementById('save-spell-button');
    const cancelEditButton = document.getElementById('cancel-edit-button');
    const spellPreviewContent = document.getElementById('spell-preview-content');
    const spellListUl = document.getElementById('spell-list');
    const selectedSpellDetailsDiv = document.getElementById('selected-spell-details');
    const addSomaticButton = document.getElementById('add-somatic-button');
    const moveRuneUpButton = document.getElementById('move-rune-up');
    const moveRuneDownButton = document.getElementById('move-rune-down');
    const removeRuneButton = document.getElementById('remove-rune');
    const copySpellButton = document.getElementById('copy-spell-button');
    const copyRunesButton = document.getElementById('copy-runes-button');
    const deleteSpellButton = document.getElementById('delete-spell-button');

    let essenceRunesData = {};       // Format: { deity: { runeKey: desc, ... }, ... }
    let incantationRunesData = {}; // Format: { runeKey: desc, ... }
    let somaticRunesData = {};     // Format: { runeKey: desc, ... }
    let spellsData = [];           // Array of spell objects from server
    let orderedFinalRunes = [];    // Array of rune *keys* (e.g., "ㄊ FÖL") in their current order for the form
    let selectedFinalRuneLi = null; // DOM element of the selected <li> in the final order list
    let currentEditingSpellIndex = null; // Index of the spell being edited from spellsData, or null if new
    let currentSelectedGrimoireLi = null; // DOM element of the selected spell in the grimoire list

    function parseInitialData() {
        const initialDataElement = document.getElementById('initial-data');
        if (initialDataElement) {
            try {
                const data = JSON.parse(initialDataElement.textContent);
                essenceRunesData = data.essence_runes || {};
                incantationRunesData = data.incantation_runes || {};
                somaticRunesData = data.somatic_runes || {};
                spellsData = data.spells || [];
                console.log("Initial data parsed successfully.");
                return true;
            } catch (e) {
                console.error("Error parsing initial data from HTML:", e);
                return false;
            }
        }
        return false;
    }

    async function fetchAllDataFromServer() {
        try {
            const [essenceRes, incantationRes, somaticRes, spellsRes] = await Promise.all([
                fetch('/api/runes/essence'),
                fetch('/api/runes/incantation'),
                fetch('/api/runes/somatic'),
                fetch('/api/spells')
            ]);
            // Check all responses are ok
            if (!essenceRes.ok) throw new Error(`Essence runes fetch failed: ${essenceRes.status}`);
            if (!incantationRes.ok) throw new Error(`Incantation runes fetch failed: ${incantationRes.status}`);
            if (!somaticRes.ok) throw new Error(`Somatic runes fetch failed: ${somaticRes.status}`);
            if (!spellsRes.ok) throw new Error(`Spells fetch failed: ${spellsRes.status}`);

            essenceRunesData = await essenceRes.json();
            incantationRunesData = await incantationRes.json();
            somaticRunesData = await somaticRes.json();
            spellsData = await spellsRes.json();
            console.log("All data fetched successfully from API endpoints.");
        } catch (error) {
            console.error("Failed to fetch initial data from API:", error);
            alert("Erreur critique: Impossible de charger les données de base des runes et des sorts. " + error.message);
        }
    }

    function populateRuneSelectionInterfaces() {
        // Essence Runes (Radio buttons)
        essenceRunesContainer.innerHTML = '';
        const essenceColumnsDiv = document.createElement('div');
        essenceColumnsDiv.className = 'essence-rune-columns';
        Object.entries(essenceRunesData).forEach(([deity, runes]) => {
            Object.entries(runes).forEach(([runeKey, desc]) => {
                const label = document.createElement('label');
                const input = document.createElement('input');
                input.type = 'radio';
                input.name = 'essence-rune';
                input.value = runeKey;
                input.dataset.runeKey = runeKey; // Store key for easier access
                input.addEventListener('change', handleEssenceOrIncantationChange);
                label.appendChild(input);
                label.appendChild(document.createTextNode(` ${runeKey} - ${desc}`));
                essenceColumnsDiv.appendChild(label);
            });
        });
        essenceRunesContainer.appendChild(essenceColumnsDiv);

        // Incantation Runes (Radio buttons, including "None")
        const noneIncantationInput = incantationRunesContainer.querySelector('input[name="incantation-rune"][value=""]');
        noneIncantationInput.addEventListener('change', handleEssenceOrIncantationChange);
        // Add other incantation runes
        Object.entries(incantationRunesData).forEach(([runeKey, desc]) => {
            const label = document.createElement('label');
            const input = document.createElement('input');
            input.type = 'radio';
            input.name = 'incantation-rune';
            input.value = runeKey;
            input.dataset.runeKey = runeKey;
            input.addEventListener('change', handleEssenceOrIncantationChange);
            label.appendChild(input);
            label.appendChild(document.createTextNode(` ${runeKey} - ${desc}`));
            incantationRunesContainer.appendChild(label);
        });

        // Somatic Runes (Select list)
        availableSomaticList.innerHTML = '';
        Object.entries(somaticRunesData).forEach(([runeKey, desc]) => {
            const option = document.createElement('option');
            option.value = runeKey;
            option.dataset.runeKey = runeKey;
            option.textContent = `${runeKey} - ${desc}`;
            availableSomaticList.appendChild(option);
        });
    }

    function getSelectedEssenceKey() {
        const selected = document.querySelector('input[name="essence-rune"]:checked');
        return selected ? selected.value : null;
    }

    function getSelectedIncantationKey() {
        const selected = document.querySelector('input[name="incantation-rune"]:checked');
        return selected ? selected.value : null; // Returns empty string for "None"
    }

    function handleEssenceOrIncantationChange() {
        const selectedEssence = getSelectedEssenceKey();
        const selectedIncantation = getSelectedIncantationKey(); // Can be ""

        // Filter out old essence/incantation, keep somatic
        let newOrderedRunes = orderedFinalRunes.filter(rk => somaticRunesData.hasOwnProperty(rk));

        if (selectedIncantation && selectedIncantation !== "") {
            newOrderedRunes.unshift(selectedIncantation); // Add incantation to the beginning if present
        }
        if (selectedEssence) {
            // Try to insert essence after incantation, or at the beginning
            if (selectedIncantation && selectedIncantation !== "") {
                newOrderedRunes.splice(1, 0, selectedEssence);
            } else {
                newOrderedRunes.unshift(selectedEssence);
            }
        }
        orderedFinalRunes = newOrderedRunes;
        renderFinalRuneOrderList();
        updateSpellPreview();
    }

    addSomaticButton.addEventListener('click', () => {
        const selectedOption = availableSomaticList.options[availableSomaticList.selectedIndex];
        if (!selectedOption) return;
        const runeKey = selectedOption.value;

        if (!orderedFinalRunes.includes(runeKey)) {
            orderedFinalRunes.push(runeKey);
            renderFinalRuneOrderList();
            updateSpellPreview();
        } else {
            alert("Cette rune somatique est déjà dans l'ordre final.");
        }
    });

    function renderFinalRuneOrderList(selectedIndexToReselect = -1) {
        finalRuneOrderListUl.innerHTML = '';
        selectedFinalRuneLi = null; // Reset selection
        orderedFinalRunes.forEach((runeKey, index) => {
            const li = document.createElement('li');
            li.dataset.runeKey = runeKey;
            li.dataset.index = index;
            li.textContent = getFullRuneDescriptionByKey(runeKey);
            
            li.addEventListener('click', (e) => {
                if (selectedFinalRuneLi) {
                    selectedFinalRuneLi.classList.remove('selected');
                }
                selectedFinalRuneLi = e.currentTarget;
                selectedFinalRuneLi.classList.add('selected');
            });

            if (index === selectedIndexToReselect) {
                li.classList.add('selected');
                selectedFinalRuneLi = li;
            }
            finalRuneOrderListUl.appendChild(li);
        });
        updateMoveRemoveButtonStates();
    }
    
    function updateMoveRemoveButtonStates() {
        const hasSelection = selectedFinalRuneLi !== null;
        moveRuneUpButton.disabled = !hasSelection || selectedFinalRuneLi.dataset.index === '0';
        moveRuneDownButton.disabled = !hasSelection || parseInt(selectedFinalRuneLi.dataset.index) === orderedFinalRunes.length - 1;
        removeRuneButton.disabled = !hasSelection;
    }

    finalRuneOrderListUl.addEventListener('click', updateMoveRemoveButtonStates); // Update on any click within list (for deselection indirect)

    removeRuneButton.addEventListener('click', () => {
        if (!selectedFinalRuneLi) return;
        const runeKeyToRemove = selectedFinalRuneLi.dataset.runeKey;
        const indexToRemove = parseInt(selectedFinalRuneLi.dataset.index);

        // Check if it's the selected essence or incantation and deselect the radio button
        if (runeKeyToRemove === getSelectedEssenceKey()) {
            const essenceRadio = document.querySelector(`input[name="essence-rune"][value="${runeKeyToRemove}"]`);
            if (essenceRadio) essenceRadio.checked = false;
        }
        if (runeKeyToRemove === getSelectedIncantationKey()) {
            document.querySelector('input[name="incantation-rune"][value=""]').checked = true; // Select "None"
        }

        orderedFinalRunes.splice(indexToRemove, 1);
        selectedFinalRuneLi = null; // Clear selection
        renderFinalRuneOrderList();
        updateSpellPreview();
    });

    moveRuneUpButton.addEventListener('click', () => moveFinalRune(-1));
    moveRuneDownButton.addEventListener('click', () => moveFinalRune(1));

    function moveFinalRune(direction) { // -1 for up, 1 for down
        if (!selectedFinalRuneLi) return;
        const currentIndex = parseInt(selectedFinalRuneLi.dataset.index);
        const newIndex = currentIndex + direction;

        if (newIndex >= 0 && newIndex < orderedFinalRunes.length) {
            const itemToMove = orderedFinalRunes.splice(currentIndex, 1)[0];
            orderedFinalRunes.splice(newIndex, 0, itemToMove);
            renderFinalRuneOrderList(newIndex); // Reselect the moved item
            updateSpellPreview();
        }
    }

    function getFullRuneDescriptionByKey(runeKey) {
        if (!runeKey) return 'Rune invalide';
        if (incantationRunesData[runeKey]) return `${runeKey} - ${incantationRunesData[runeKey]}`;
        if (somaticRunesData[runeKey]) return `${runeKey} - ${somaticRunesData[runeKey]}`;
        for (const deity in essenceRunesData) {
            if (essenceRunesData[deity][runeKey]) return `${runeKey} - ${essenceRunesData[deity][runeKey]}`;
        }
        const keyPart = runeKey.split(' ')[0] || runeKey;
        return `${keyPart} - Description inconnue`;
    }

    function updateSpellPreview() {
        const pronunciationParts = [];
        const gestures = [];
        let essencePresentInOrder = false;

        orderedFinalRunes.forEach(runeKey => {
            const syllable = runeKey.split(' ')[1] || runeKey; // Assumes "SYMBOL KEY" or just "KEY"
            pronunciationParts.push(syllable);

            if (incantationRunesData[runeKey]) {
                gestures.push(incantationRunesData[runeKey]);
            }
            if (somaticRunesData[runeKey]) {
                gestures.push(somaticRunesData[runeKey]);
            }
            if (getSelectedEssenceKey() === runeKey) {
                essencePresentInOrder = true;
            }
        });
        
        const selectedEssence = getSelectedEssenceKey();
        if (!selectedEssence) {
            spellPreviewContent.innerHTML = '<p>(Sélectionnez une rune d\'essence pour voir l\'aperçu)</p>';
            return;
        }
        // If an essence is selected but not yet in orderedFinalRunes (e.g. immediately after radio click)
        // we should still show its syllable for pronunciation preview
        let finalPronunciationParts = [...pronunciationParts];
        if (selectedEssence && !orderedFinalRunes.includes(selectedEssence)) {
            const essenceSyllable = selectedEssence.split(' ')[1] || selectedEssence;
            // Attempt to insert it logically or just add if complex
            const incantationKey = getSelectedIncantationKey();
            let essenceInserted = false;
            if (incantationKey && orderedFinalRunes.includes(incantationKey)){
                const incIndex = finalPronunciationParts.indexOf(incantationKey.split(' ')[1] || incantationKey);
                if(incIndex !== -1){
                    finalPronunciationParts.splice(incIndex + 1, 0, essenceSyllable);
                    essenceInserted = true;
                }
            }
            if(!essenceInserted){
                 finalPronunciationParts.unshift(essenceSyllable); // Default to start if no incantation or complex
            }
             finalPronunciationParts = [...new Set(finalPronunciationParts)]; // Remove duplicates if any due to timing
        }

        let previewHTML = `<p><strong>Prononciation:</strong> ${finalPronunciationParts.join('-')}</p>`;
        previewHTML += '<p><strong>Gestes à réaliser (ordre important):</strong></p>';
        if (gestures.length === 0 && (!orderedFinalRunes.some(r => incantationRunesData[r] || somaticRunesData[r]))) {
             previewHTML += '<p>(Aucun geste identifié)</p>';
        } else if (gestures.length === 0 && orderedFinalRunes.some(r => incantationRunesData[r] || somaticRunesData[r])) {
            // This case can happen if gestures are only from incantation/somatic not yet in the `gestures` array from the loop
            // but are in `orderedFinalRunes`. Re-evaluate gestures based on `orderedFinalRunes` for preview accuracy.
            const actualGestures = orderedFinalRunes
                .map(rk => incantationRunesData[rk] || somaticRunesData[rk])
                .filter(Boolean);
            if (actualGestures.length === 0) {
                 previewHTML += '<p>(Aucun geste supplémentaire)</p>';
            } else {
                previewHTML += '<ul>';
                actualGestures.forEach((g, i) => previewHTML += `<li>${i + 1}. ${g}</li>`);
                previewHTML += '</ul>';
            }
        } else if (gestures.length > 0) {
            previewHTML += '<ul>';
            gestures.forEach((g, i) => previewHTML += `<li>${i + 1}. ${g}</li>`);
            previewHTML += '</ul>';
        }
        spellPreviewContent.innerHTML = previewHTML;
    }

    spellForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const name = spellNameInput.value.trim();
        const description = spellDescriptionInput.value.trim();
        const essence = getSelectedEssenceKey();

        if (!name || !description) {
            alert("Le nom et la description sont requis.");
            return;
        }
        if (!essence) {
            alert("Une rune d'essence est obligatoire.");
            return;
        }
        if (!orderedFinalRunes.includes(essence)) {
            alert("La rune d'essence sélectionnée doit être présente dans l'ordre final des runes.");
            return;
        }

        const spellPayload = {
            name: name,
            description: description,
            essence: essence, // The key of the chosen essence rune
            incantation: getSelectedIncantationKey() || null, // null if "None" (empty string value)
            somatic_runes: orderedFinalRunes.filter(rk => somaticRunesData.hasOwnProperty(rk)),
            ordered_runes: orderedFinalRunes
        };

        try {
            let response;
            let url = '/api/spell';
            let method = 'POST';

            if (currentEditingSpellIndex !== null) {
                url = `/api/spell/${currentEditingSpellIndex}`;
                method = 'PUT';
            }

            response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(spellPayload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.description || `Erreur Serveur: ${response.status}`);
            }
            const savedSpell = await response.json();
            alert(`Sortilège "${savedSpell.name}" ${currentEditingSpellIndex !== null ? 'modifié' : 'créé'} avec succès!`);
            
            // Update client-side data and UI
            if (currentEditingSpellIndex !== null) {
                spellsData[currentEditingSpellIndex] = savedSpell;
            } else {
                spellsData.push(savedSpell);
            }
            resetFormAndUI();
            refreshGrimoireSpellList();
            // Optionally, re-select and display the new/edited spell in grimoire
            const newIndex = spellsData.findIndex(s => s.name === savedSpell.name && s.pronunciation === savedSpell.pronunciation); // A bit fragile
            if (newIndex !== -1) {
                selectSpellInGrimoire(newIndex);
            }
            // Update the bottom-left preview with full details of the created/saved spell
            displayFullSpellDetailsInPreview(savedSpell);

        } catch (error) {
            console.error("Erreur lors de la sauvegarde du sortilège:", error);
            alert("Erreur lors de la sauvegarde du sortilège: " + error.message);
        }
    });
    
    function displayFullSpellDetailsInPreview(spell) {
        if (!spell) {
            spellPreviewContent.innerHTML = '<p>(Aucun sort à afficher)</p>';
            return;
        }
        let detailsHTML = `<p><strong>Nom:</strong> ${spell.name}</p>`;
        detailsHTML += `<p><strong>Description:</strong> ${spell.description}</p>`;
        detailsHTML += `<p><strong>Essence:</strong> ${getFullRuneDescriptionByKey(spell.essence)}</p>`;
        const incantationDesc = spell.incantation ? getFullRuneDescriptionByKey(spell.incantation) : 'Aucune';
        detailsHTML += `<p><strong>Incantation:</strong> ${incantationDesc}</p>`;
        const somaticsDesc = spell.somatic_runes && spell.somatic_runes.length > 0 
            ? spell.somatic_runes.map(rKey => getFullRuneDescriptionByKey(rKey)).join(', ') 
            : 'Aucune';
        detailsHTML += `<p><strong>Runes Somatiques (liste):</strong> ${somaticsDesc}</p>`;
        detailsHTML += `<p><strong>Ordre Final des Runes:</strong> ${spell.ordered_runes.map(rKey => rKey.split(' ')[0] || rKey).join(' ')}</p>`;
        detailsHTML += `<p><strong>Prononciation Complète:</strong> ${spell.pronunciation}</p>`;
        detailsHTML += '<p><strong>Gestes à Réaliser (ordre):</strong></p>';
        if (spell.gestures && spell.gestures.length > 0) {
            detailsHTML += '<ul>';
            spell.gestures.forEach((g, i) => detailsHTML += `<li>${i + 1}. ${g}</li>`);
            detailsHTML += '</ul>';
        } else {
            detailsHTML += '<p>(Aucun geste spécifique listé)</p>';
        }
        spellPreviewContent.innerHTML = detailsHTML;
    }

    function resetFormAndUI(clearGrimoireSelection = false) {
        spellForm.reset();
        orderedFinalRunes = [];
        selectedFinalRuneLi = null;
        renderFinalRuneOrderList(); 
        updateSpellPreview(); 
        
        // Explicitly deselect radio buttons
        document.querySelectorAll('input[name="essence-rune"]:checked').forEach(rb => rb.checked = false);
        const noneIncantationRadio = document.querySelector('input[name="incantation-rune"][value=""]');
        if (noneIncantationRadio) noneIncantationRadio.checked = true;
        
        currentEditingSpellIndex = null;
        createSpellButton.style.display = 'inline-block';
        saveSpellButton.style.display = 'none';
        cancelEditButton.style.display = 'none';
        
        if(clearGrimoireSelection){
            if (currentSelectedGrimoireLi) {
                currentSelectedGrimoireLi.classList.remove('selected');
                currentSelectedGrimoireLi = null;
            }
            selectedSpellDetailsDiv.innerHTML = '<p>(Sélectionnez un sort pour voir ses détails)</p>';
            disableGrimoireActionButtons();
        }
        spellNameInput.focus();
        updateMoveRemoveButtonStates(); // Ensure these are disabled
    }
    
    cancelEditButton.addEventListener('click', () => {
        // If a spell was selected in grimoire, restore form to that spell, otherwise clear to new spell form.
        if(currentSelectedGrimoireLi && currentEditingSpellIndex !== null) {
            // We were editing a spell selected from the grimoire
            fillFormForEditing(spellsData[currentEditingSpellIndex], currentEditingSpellIndex);
        } else {
            // Not editing or no grimoire selection, just reset to blank create form
            resetFormAndUI(true); // true to clear grimoire selection as well
        }
    });

    function refreshGrimoireSpellList() {
        spellListUl.innerHTML = '';
        spellsData.forEach((spell, index) => {
            const li = document.createElement('li');
            li.textContent = spell.name;
            li.dataset.spellIndex = index;
            li.addEventListener('click', () => selectSpellInGrimoire(index));
            spellListUl.appendChild(li);
        });
        // If we were editing, try to reselect
        if (currentEditingSpellIndex !== null && spellsData[currentEditingSpellIndex]) {
            const itemToReselect = spellListUl.querySelector(`li[data-spell-index="${currentEditingSpellIndex}"]`);
            if(itemToReselect) {
                itemToReselect.classList.add('selected');
                currentSelectedGrimoireLi = itemToReselect;
            }
        } else {
            currentSelectedGrimoireLi = null; // Ensure no stale selection display
            disableGrimoireActionButtons();
        }
    }

    function selectSpellInGrimoire(index) {
        if (index < 0 || index >= spellsData.length) return;
        const spell = spellsData[index];
        if (!spell) return;

        if (currentSelectedGrimoireLi) {
            currentSelectedGrimoireLi.classList.remove('selected');
        }
        currentSelectedGrimoireLi = spellListUl.querySelector(`li[data-spell-index="${index}"]`);
        if (currentSelectedGrimoireLi) {
            currentSelectedGrimoireLi.classList.add('selected');
        }
        
        displaySpellInGrimoireDetails(spell);
        fillFormForEditing(spell, index);
        enableGrimoireActionButtons();
    }

    function displaySpellInGrimoireDetails(spell) {
        let detailsHTML = `<p><strong>Nom:</strong> ${spell.name}</p>`;
        detailsHTML += `<p><strong>Description:</strong> ${spell.description}</p>`;
        detailsHTML += `<p><strong>Essence:</strong> ${getFullRuneDescriptionByKey(spell.essence)}</p>`;
        const incantationDesc = spell.incantation ? getFullRuneDescriptionByKey(spell.incantation) : 'Aucune';
        detailsHTML += `<p><strong>Incantation:</strong> ${incantationDesc}</p>`;
        const somaticsDesc = spell.somatic_runes && spell.somatic_runes.length > 0 
            ? spell.somatic_runes.map(rKey => getFullRuneDescriptionByKey(rKey)).join(', ') 
            : 'Aucune';
        detailsHTML += `<p><strong>Runes Somatiques (liste):</strong> ${somaticsDesc}</p>`;
        detailsHTML += `<p><strong>Ordre Final des Runes:</strong> ${spell.ordered_runes.map(rKey => rKey.split(' ')[0] || rKey).join(' ')}</p>`;
        detailsHTML += `<p><strong>Prononciation Complète:</strong> ${spell.pronunciation}</p>`;
        detailsHTML += '<p><strong>Gestes à Réaliser (ordre):</strong></p>';
        if (spell.gestures && spell.gestures.length > 0) {
            detailsHTML += '<ul>';
            spell.gestures.forEach((g,i) => detailsHTML += `<li>${i+1}. ${g}</li>`);
            detailsHTML += '</ul>';
        } else {
            detailsHTML += '<p>(Aucun geste spécifique listé)</p>';
        }
        selectedSpellDetailsDiv.innerHTML = detailsHTML;
    }

    function fillFormForEditing(spell, index) {
        resetFormAndUI(); // Start with a clean slate, then populate
        
        spellNameInput.value = spell.name;
        spellDescriptionInput.value = spell.description;
        currentEditingSpellIndex = index;

        if (spell.essence) {
            const essenceRadio = document.querySelector(`input[name="essence-rune"][value="${spell.essence}"]`);
            if (essenceRadio) essenceRadio.checked = true;
        }
        const incantationToSet = spell.incantation || ""; // Ensure empty string for "None"
        const incantationRadio = document.querySelector(`input[name="incantation-rune"][value="${incantationToSet}"]`);
        if (incantationRadio) incantationRadio.checked = true;
        
        orderedFinalRunes = [...spell.ordered_runes]; // Crucial: copy the array
        renderFinalRuneOrderList();
        updateSpellPreview(); // Update preview based on loaded spell

        createSpellButton.style.display = 'none';
        saveSpellButton.style.display = 'inline-block';
        saveSpellButton.textContent = 'Sauvegarder les Modifications';
        cancelEditButton.style.display = 'inline-block';
    }
    
    function enableGrimoireActionButtons(){
        copySpellButton.disabled = false;
        copyRunesButton.disabled = false;
        deleteSpellButton.disabled = false;
    }
    function disableGrimoireActionButtons(){
        copySpellButton.disabled = true;
        copyRunesButton.disabled = true;
        deleteSpellButton.disabled = true;
    }

    copySpellButton.addEventListener('click', async () => {
        if (currentEditingSpellIndex === null || !spellsData[currentEditingSpellIndex]) {
            alert("Veuillez sélectionner un sort à copier depuis le grimoire.");
            return;
        }
        const spell = spellsData[currentEditingSpellIndex];
        const runeSymbols = spell.ordered_runes.map(rKey => rKey.split(' ')[0] || rKey);
        const runesText = runeSymbols.join(' ');
        const copyText = `Nom: ${spell.name}\nRunes: ${runesText}\nDescription: ${spell.description}`;
        try {
            await navigator.clipboard.writeText(copyText);
            alert("Détails du sortilège copiés dans le presse-papiers!");
        } catch (err) {
            console.error('Échec de la copie du sort: ', err);
            alert("Erreur lors de la copie du sort.");
        }
    });

    copyRunesButton.addEventListener('click', async () => {
        if (currentEditingSpellIndex === null || !spellsData[currentEditingSpellIndex]) {
            alert("Veuillez sélectionner un sort pour copier ses runes depuis le grimoire.");
            return;
        }
        const spell = spellsData[currentEditingSpellIndex];
        const runeSymbols = spell.ordered_runes.map(rKey => rKey.split(' ')[0] || rKey);
        const runesText = runeSymbols.join(' ');
        try {
            await navigator.clipboard.writeText(runesText);
            alert("Runes du sortilège copiées dans le presse-papiers!");
        } catch (err) {
            console.error('Échec de la copie des runes: ', err);
            alert("Erreur lors de la copie des runes.");
        }
    });

    deleteSpellButton.addEventListener('click', async () => {
        if (currentEditingSpellIndex === null || !spellsData[currentEditingSpellIndex]) {
            alert("Veuillez sélectionner un sort à supprimer depuis le grimoire.");
            return;
        }
        const spellToDelete = spellsData[currentEditingSpellIndex];
        if (!confirm(`Êtes-vous sûr de vouloir supprimer le sort "${spellToDelete.name}"? Cette action est irréversible.`)) {
            return;
        }
        try {
            const response = await fetch(`/api/spell/${currentEditingSpellIndex}`, { method: 'DELETE' });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.description || `Erreur Serveur: ${response.status}`);
            }
            alert(`Sortilège "${spellToDelete.name}" supprimé avec succès.`);
            
            // Update client-side data and UI
            spellsData.splice(currentEditingSpellIndex, 1);
            resetFormAndUI(true); // true to clear grimoire selection as well
            refreshGrimoireSpellList(); // Refresh grimoire
            // currentEditingSpellIndex is now invalid, handled by resetFormAndUI

        } catch (error) {
            console.error("Erreur lors de la suppression du sort:", error);
            alert("Erreur lors de la suppression du sort: " + error.message);
        }
    });

    async function initializeApp() {
        const dataParsedFromHTML = parseInitialData();
        if (!dataParsedFromHTML) {
            // Fallback to fetching all data if HTML parsing failed or data wasn't there
            await fetchAllDataFromServer();
        }
        populateRuneSelectionInterfaces();
        refreshGrimoireSpellList();
        resetFormAndUI(true); // Start with a clean form and no grimoire selection
        updateMoveRemoveButtonStates(); // Ensure order buttons are correctly disabled initially
    }

    initializeApp();
}); 