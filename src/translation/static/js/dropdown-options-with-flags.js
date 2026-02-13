// If no cookie is found on the device with the previous language selection then it will use the default settings
const defaultSelection = {
  'translateFrom': 'us',
  'translateTo': 'es'
};

const languages = {
  'us': {
    'readableName': 'English',
    'flagCode': 'us',
    'translateFrom': 'en-US',
    'translateTo': 'en-US_M_Neural_B_0013'
  },

  'es': {
    'readableName': 'Spanish',
    'flagCode': 'es',
    'translateFrom': 'es-ES',
    'translateTo': 'es-US_M_Neural_D_0008'
  },

  'pl': {
    'readableName': 'Polish',
    'flagCode': 'pl',
    'translateFrom': 'pl-PL',
    'translateTo': 'pl-PL_M_Standard_D_0008'
  },

  // Doesn't work for some reason when set in "Translate From"
  // 'rs': {
  //   'readableName': 'Serbian',
  //   'flagCode': 'rs',
  //   'translateFrom': 'sr-RS',
  //   'translateTo': 'sr-RS_F_Standard_D_0001'
  // },

  'ru': {
    'readableName': 'Russian',
    'flagCode': 'ru',
    'translateFrom': 'ru-RU',
    'translateTo': 'ru-RU_M_Neural_D_0010'
  }
};

var translationState = {
  'currentTranslateFrom': null,
  'currentTranslateTo': null
};

const dropdowns = ['translateTo', 'translateFrom']; // IDs of all select elements

document.addEventListener("DOMContentLoaded", function() {  
    dropdowns.forEach(function(dropdownId) {
      const selectElement = document.getElementById(dropdownId);
      if (!selectElement) return;
      const selectParent = selectElement.parentNode;
      const selectedLanguageCookie = getCookie(dropdownId);
  
      const customDropdown = document.createElement("div");
      customDropdown.className = "dropdown";
  
      const dropdownButton = document.createElement("button");
      dropdownButton.id = dropdownId + 'Button';
      dropdownButton.className = "btn dropdown-toggle";
      dropdownButton.setAttribute("type", "button");
      dropdownButton.setAttribute("data-bs-toggle", "dropdown");
      dropdownButton.setAttribute("aria-expanded", "false");
  
      const dropdownMenu = document.createElement("ul");
      dropdownMenu.className = "dropdown-menu";
  
      dropdownButton.className += ` ${selectElement.className}`;
      dropdownButton.classList.remove("form-select");
  
      customDropdown.appendChild(dropdownButton);
      customDropdown.appendChild(dropdownMenu);
  
      selectParent.insertBefore(customDropdown, selectElement.nextSibling);
      selectElement.style.display = "none";

      var selectionId = null;

      if(dropdownButton.id == 'translateToButton') {
        selectionId = 'translateTo';
      }
      
      if (dropdownButton.id == 'translateFromButton') {
        selectionId = 'translateFrom';
      }
      
      if(selectionId === null) return;
      
      // Assuming selectElement and dropdownMenu are defined elsewhere in your code
      Object.keys(languages).forEach(key => {
        const languageSetting = languages[key];

        const optionText = languageSetting['readableName'];
        const flagCode = languageSetting['flagCode'];
        const flagUrl = `${window.location.origin}/static/flags/4x3/${flagCode}.svg`;

        const listItem = document.createElement("li");
        const link = document.createElement("a");
        link.classList.add(selectionId);
        link.id = flagCode;
        link.href = "#";
        link.innerHTML = `<div style="display: flex; align-items: center; gap: 10px;"><img src="${flagUrl}" class="flag-icon" style="width:20px;"> ${optionText}</div>`;
        link.classList.add("dropdown-item");
        link.addEventListener("click", function(e) {
          e.preventDefault();
          selectElement.value = key;
          updateDropdownButton(dropdownButton, flagCode, optionText);
        });
        listItem.appendChild(link);
        dropdownMenu.appendChild(listItem);
      
        if (key === selectedLanguageCookie) {
          updateDropdownButton(dropdownButton, flagCode, optionText);
          selectElement.value = key;
        }
      });
  
      // Set default selected option from the original select element if no cookie is set
      if (selectedLanguageCookie) return;
      
      const languageSetting = languages[defaultSelection[selectionId]];
      
      const flagCode = languageSetting['flagCode'];
      const selectedText = languageSetting['readableName'];

      updateDropdownButton(dropdownButton, flagCode, selectedText);
      
    });


  });

  function setCookie(name, value, days) {
    let expires = "";
    if (days) {
      let date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
  }

  function getCookie(name) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i].trim();
      if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length);
    }
    return null;
  }

  function updateDropdownButton(button, flagCode, optionText=null) {
    const flagUrl = `${window.location.origin}/static/flags/4x3/${flagCode}.svg`;

    const translateFrom = languages[flagCode]['translateFrom'];
    const translateTo = languages[flagCode]['translateTo'];

    var cookie = 'null';

    if(button.id == 'translateFromButton') {
      cookie = 'translateFrom';
      translationState['currentTranslateFrom'] = flagCode;
      document.getElementById('translateFromInput').value = translateFrom;
    }
      
    if(button.id == 'translateToButton') {
      cookie = 'translateTo';
      translationState['currentTranslateTo'] = flagCode;
      document.getElementById('translateToInput').value = translateTo;
    }

    button.innerHTML = '';
  
    // Create a span for text and image
    const contentSpan = document.createElement('span');
    contentSpan.style.display = 'flex';
    contentSpan.style.alignItems = 'center';
    contentSpan.style.gap = '10px';
  
    // Add the flag icon
    const img = document.createElement('img');
    img.src = flagUrl;
    img.classList.add('flag-icon');
    img.style.width = '20px';
    contentSpan.appendChild(img);

    if(optionText === null) {
      optionText = languages[flagCode]['readableName'];
    }
  
    // Add the text
    const textNode = document.createTextNode(optionText);
    contentSpan.appendChild(textNode);
  
    // Append the span to the button
    button.appendChild(contentSpan);
  
    // Apply flex layout to keep everything in line, including the ::after element
    button.style.display = 'flex';
    button.style.justifyContent = 'space-between';
    button.style.alignItems = 'center';
    button.style.width = '100%'; // Ensure the button stretches to full width if needed

    setCookie(cookie, flagCode, 7);
  }

  function swapLanguages() {
    if (!translationState.currentTranslateFrom || !translationState.currentTranslateTo) {
      console.error('Both translateFrom and translateTo need to be selected before swapping.');
      return;
    }

    [translationState.currentTranslateFrom, translationState.currentTranslateTo] =
    [translationState.currentTranslateTo, translationState.currentTranslateFrom];

    const translateFromButton = document.getElementById('translateFromButton');
    const translateToButton = document.getElementById('translateToButton');
    
    updateDropdownButton(translateFromButton, translationState.currentTranslateFrom);
    updateDropdownButton(translateToButton, translationState.currentTranslateTo);
  }