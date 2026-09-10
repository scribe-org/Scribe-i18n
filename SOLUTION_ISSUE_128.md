# Solution for Issue #128

## 🛠️ Proposed Solution (by Aditya Waghamare)

### Analysis
The `scribe-org/Scribe-i18n` repository manages internationalization (i18n) strings for Scribe. Expanding support for Hindi (`hi`) requires adding the Hindi locale configuration, ensuring locale imports/exports are updated, and adding initial translation keys in JSON format for the Hindi locale so that users can view and contribute Hindi translations.

### Fix
Add Hindi (`hi`) locale support to `src/locales/hi.json` (or the equivalent locale registration file) and register it in the main i18n configuration index.

### Implementation
```json
{
  "language": "Hindi",
  "code": "hi",
  "translations": {
    "welcome": "स्क्राइब में आपका स्वागत है",
    "description": "सुलभ और समावेशी पठन और लेखन सहायक",
    "settings": "सेटिंग्स",
    "language": "भाषा",
    "help": "सहायता"
  }
}
```

And in the supported locales configuration:
```javascript
import hi from './locales/hi.json';

export const locales = {
  // ... existing locales
  hi,
};
```

### Testing
Verify that `hi` is included in the supported locale list and that Hindi translation keys load correctly without missing translation warnings.

Signed-off-by: Aditya Waghamare <adityawaghamare7620@gmail.com>

---
*Submitted by Aditya Waghamare*
💰 **Payout Address (Base L2 / EVM):** `0xb61dBcdBc3407F71EaCb64D4CBFAcf9FFfe2415C`