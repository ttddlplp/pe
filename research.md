# Feasibility Study: Building a Custom Telegram Client

## 1. Telegram's Open Source Availability

Telegram publishes the source code for all its official client applications. The key repositories are:

**iOS:**
- [TelegramMessenger/Telegram-iOS](https://github.com/TelegramMessenger/Telegram-iOS) -- the current official iOS client. ~70% Swift, ~24% Objective-C, ~5M lines of code, 229 modules. Licensed under **GPL v2**.

**Android:**
- [DrKLO/Telegram](https://github.com/DrKLO/Telegram) -- official Android client. Java/Kotlin with native C/C++ (JNI) for crypto. Licensed under **GPL v2 or later**.

**Android (Telegram X):**
- [TGX-Android/Telegram-X](https://github.com/TGX-Android/Telegram-X) -- official alternative Android client built on TDLib. Licensed under **GPL v3**.

**Desktop:**
- [telegramdesktop/tdesktop](https://github.com/telegramdesktop/tdesktop) -- Qt-based desktop client for Windows, macOS, Linux. Licensed under **GPL v3**.

**macOS (native):**
- [overtake/TelegramSwift](https://github.com/overtake/TelegramSwift) -- native macOS client in Swift 5.0. Licensed under **GPL v2**.

**Web:**
- Telegram Web Version K and Version A -- both licensed under **GPL v3**.

**TDLib:**
- [tdlib/td](https://github.com/tdlib/td) -- cross-platform library for building Telegram clients. Licensed under **Boost Software License 1.0** (very permissive).

**Other:**
- Unigram (Windows, GPL v3), MadelineProto (PHP, AGPL v3), CLI client (Linux, GPL v2).

Telegram also supports **reproducible builds** so anyone can verify the App Store / Play Store binaries match the published source code.

---

## 2. How Nicegram and Similar Apps Work

Custom clients like Nicegram are **direct forks** of Telegram's official source code. The workflow is:

1. **Fork the official repo** (e.g., `TelegramMessenger/Telegram-iOS` or `DrKLO/Telegram`).
2. **Obtain your own `api_id` and `api_hash`** from [my.telegram.org](https://my.telegram.org).
3. **Modify the codebase** -- add features, change UI, integrate additional services.
4. **Rebrand** -- new name, new icon (cannot use "Telegram" or its logo).
5. **Publish source code** to comply with the GPL license.
6. **Distribute** via app stores.

**Typical customizations include:**
- Unlock content filters (Nicegram's original value proposition)
- Additional privacy controls (hide typing indicators, control read receipts, "last seen" hiding)
- Built-in message translation
- UI/theme customization and additional appearance options
- Chat organization tools (folders, tabs)
- Business/productivity features (Nicegram added AI tools, Web3 integrations)
- Faster animations, performance tweaks

**Nicegram specifically** has evolved into a business-oriented messaging platform with AI features, financial tools, and what they call "Nicegram OS" -- an operating system layer on top of Telegram for productivity.

**Swiftgram** was created by the original Nicegram creator as a successor project, also forking `Telegram-iOS`.

The key principle: forks stay **fully compatible** with Telegram's network -- all messages, contacts, groups, etc. work across all clients because they all connect to the same Telegram backend.

---

## 3. TDLib (Telegram Database Library)

TDLib is a **cross-platform, fully-featured Telegram client library** that abstracts away all the complexity of the MTProto protocol, encryption, and local data storage.

**What it handles:**
- Network communication with Telegram servers
- MTProto protocol implementation
- End-to-end encryption
- Local database/cache management
- File management (uploads/downloads)
- All Telegram API methods

**Platform support:** Android, iOS, Windows, macOS, Linux, WebAssembly, FreeBSD, watchOS, tvOS, Tizen, and more.

**Language bindings:**
- Native C++ interface
- Native Java interface (JNI)
- Native .NET interface (C++/CLI)
- JSON interface (usable from any language that can call C functions)
- Community wrappers: Rust (`rust-tdlib`), Node.js (`tglib`), Python, Julia, Go, and many more.

**Two approaches to building a custom client:**

| Approach | Fork Official App | Build from Scratch with TDLib |
|---|---|---|
| **Effort** | Lower -- existing UI/UX done | Much higher -- build all UI from zero |
| **Time to market** | Weeks to months | Many months to years |
| **Customizability** | Constrained by existing architecture | Total freedom |
| **Maintenance** | Must merge upstream changes | Must implement new Telegram features yourself |
| **Complexity** | Must understand massive existing codebase | Simpler dependency but more work overall |
| **License** | GPL (must open source) | Boost 1.0 (can be proprietary) |

TDLib is notably used by Telegram X (the official alternative Android client) and Unigram (Windows client). An example of a from-scratch client is [BetterTG](https://github.com/levochkaa/BetterTG), built entirely in SwiftUI using TDLib.

**Key TDLib advantage:** The Boost 1.0 license means you can build a proprietary client on TDLib without open-sourcing your code (unlike forking the GPL-licensed official apps).

---

## 4. Legal/Policy Considerations

### Telegram API Terms of Service

**Registration requirement:** You **must** obtain your own `api_id` from [my.telegram.org](https://my.telegram.org). The sample API ID included in source code is rate-limited and will cause `API_ID_PUBLISHED_FLOOD` errors. Each app needs its own credentials.

**Branding rules:**
- App title **must not** include "Telegram" unless preceded by "Unofficial" (e.g., "Unofficial Telegram Client: MyApp")
- **Cannot** use the official Telegram logo (white paper plane in blue circle) -- both are registered trademarks
- Must clearly state in app store descriptions and in-app intro that the app uses the Telegram API

**Feature requirements:**
- All **basic Telegram features must work correctly** and compatibly with other Telegram clients
- **Forbidden to:** force other users to download your app to view content, interfere with self-destructing messages, tamper with read receipts, fake last-seen/online status, or take actions on behalf of users without consent

**Privacy obligations:**
- Must comply with Telegram's Security Guidelines
- Must protect user data and privacy

**Monetization:**
- Allowed through advertising or "other legitimate means"
- Must disclose all monetization methods in app store descriptions

**Enforcement:**
- All unofficial client accounts are **automatically put under observation**
- Violations result in a 10-day notice to fix issues
- Failure to comply leads to API access revocation and app store removal requests
- Telegram reserves the right to expand terms at any time

**GPL compliance:** If you fork the official apps (GPL v2/v3), you **must** publish your source code. TDLib (Boost license) does not have this requirement.

---

## 5. Technical Requirements

### iOS Client (Forking Telegram-iOS)

| Component | Requirement |
|---|---|
| **Language** | Swift (~70%), Objective-C (~24%), C/C++ |
| **Build System** | Bazel (managed via Python scripts) |
| **IDE** | Xcode (specific version per release, check `versions.json`) |
| **OS** | macOS (specific version per release) |
| **Other** | Python 3, Git, Apple Developer account |
| **Key libraries** | OpenSSL, FFmpeg, WebRTC |
| **Codebase size** | ~5M lines, 229 modules |

Build process:
1. `git clone --recursive -j8` the repo
2. Configure `template_minimal_development_configuration.json` with your API ID, team ID, etc.
3. Run `python3 build-system/Make/Make.py generateProject ...`
4. Build/run in Xcode (simulator works with ad-hoc signing)

### Android Client (Forking DrKLO/Telegram)

| Component | Requirement |
|---|---|
| **Language** | Java, Kotlin, C/C++ (JNI) |
| **Build System** | Gradle |
| **IDE** | Android Studio 3.4+ |
| **NDK** | Android NDK rev. 20 |
| **SDK** | Android SDK 8.1+ |
| **Other** | Firebase (for push notifications), release keystore |

Build process:
1. Clone repo, configure `gradle.properties` with keystore info
2. Set up Firebase, download `google-services.json`
3. Fill out `BuildVars.java` with API credentials
4. Open (not import) in Android Studio and build

### Development Effort Estimate

- **Fork with minor UI changes:** 2-4 weeks for an experienced mobile developer
- **Fork with significant feature additions:** 2-6 months
- **From-scratch client using TDLib:** 6-18+ months for a full-featured client
- **Ongoing maintenance:** Continuous -- Telegram updates frequently and you must keep up with protocol changes, new features, and security patches. This is the **most underestimated cost**.

---

## 6. Distribution

### Google Play
- Custom Telegram clients **can** be published. Multiple exist: Nicegram, Plus Messenger, Nekogram, Graph Messenger, Forkgram.
- Must comply with Google Play policies (content moderation, privacy policy, etc.)
- Risk of removal if Telegram content moderation issues arise (precedent: Telegram X was temporarily removed from Play Store in late 2025 due to potential licensing conflicts).

### Apple App Store
- Custom Telegram clients **can** be published. Nicegram is available on the App Store.
- Apple has stricter review processes. Historical precedent: both Telegram and Telegram X were removed in 2018 due to child exploitation content being shared via public channels, and were only restored after Telegram added filtering.
- Review times are typically 24-48 hours but can vary.
- Must comply with Apple's guidelines around duplicate apps, spam apps, etc.

### Known Distribution Issues
- **App store gatekeeping:** Both Apple and Google can remove apps with little transparency, and messaging apps face heightened scrutiny around content moderation.
- **Telegram X precedent:** Was removed and re-added to Play Store, showing that even official alternative clients face distribution risk.
- **Content moderation requirements:** App stores may hold your client responsible for content accessible through the Telegram network.

### Alternative Distribution
- **F-Droid** (Android) -- popular for open-source clients like Nekogram
- **Direct APK distribution** (Android) -- via developer websites
- **Telegram Mini Apps** -- an entirely different approach that avoids app stores altogether, running inside Telegram itself

---

## 7. Key Open Source Repositories

### Official Telegram Repos

| Repository | Platform | License | URL |
|---|---|---|---|
| Telegram-iOS | iOS | GPL v2 | [TelegramMessenger/Telegram-iOS](https://github.com/TelegramMessenger/Telegram-iOS) |
| Telegram Android | Android | GPL v2+ | [DrKLO/Telegram](https://github.com/DrKLO/Telegram) |
| Telegram X | Android | GPL v3 | [TGX-Android/Telegram-X](https://github.com/TGX-Android/Telegram-X) |
| Telegram Desktop | Win/Mac/Linux | GPL v3 | [telegramdesktop/tdesktop](https://github.com/telegramdesktop/tdesktop) |
| Telegram macOS | macOS | GPL v2 | [overtake/TelegramSwift](https://github.com/overtake/TelegramSwift) |
| TDLib | Cross-platform | Boost 1.0 | [tdlib/td](https://github.com/tdlib/td) |

### Notable Third-Party Clients

| Client | Platform | Focus | URL |
|---|---|---|---|
| Nicegram | iOS/Android/Desktop | Business, AI, Web3 | [nicegram on GitHub](https://github.com/nicegram) |
| Swiftgram | iOS | Enhanced features (by original Nicegram creator) | [Swiftgram/Telegram-iOS](https://github.com/Swiftgram/Telegram-iOS) |
| Nekogram | Android | Privacy, translation | [Nekogram/Nekogram](https://github.com/Nekogram/Nekogram) |
| Plus Messenger | Android | UI customization | Closed source (Play Store) |
| Graph Messenger | Android | Advanced controls | Play Store |
| Forkgram | Android | Lightweight mods | [Forkgram/TelegramAndroid](https://github.com/Forkgram/TelegramAndroid) |
| Unigram | Windows | Native Windows UX | GPL v3 |
| Kotatogram | Desktop | Hotkeys, power users | GitHub |
| BetterTG | iOS | SwiftUI + TDLib (from scratch) | [levochkaa/BetterTG](https://github.com/levochkaa/BetterTG) |
| Teamgram | Server | Unofficial MTProto server in Go | [teamgram on GitHub](https://github.com/teamgram) |

---

## 8. Risks and Challenges

### Technical Risks
- **Massive codebase complexity:** The iOS client alone is ~5M lines with 229 modules. Understanding and modifying it safely is non-trivial.
- **Build system complexity:** Bazel (iOS) and the specific NDK/SDK requirements (Android) create a steep initial setup. Build environments must exactly match version requirements.
- **Upstream merge burden:** Telegram updates frequently. Keeping your fork in sync with upstream changes while preserving your modifications is the single largest ongoing technical cost. Merge conflicts are guaranteed.
- **Protocol changes:** Telegram can change their MTProto protocol or API layers, potentially breaking custom clients without warning.
- **Third-party library dependencies:** OpenSSL, FFmpeg, WebRTC -- all must be compiled and maintained for target platforms.

### Business Risks
- **Account bans:** All accounts using unofficial clients are automatically flagged for observation. Users of your app may get banned, especially if behavior patterns look suspicious. Recovery requires emailing `recover@telegram.org` and is not guaranteed.
- **API access revocation:** Telegram can revoke your `api_id` with 10 days notice if they determine you violate their ToS, killing your entire product.
- **App store removal:** Both Apple and Google can remove your app. Telegram has leverage to request removal. Content moderation issues on the Telegram network (which you don't control) can cause your app to be pulled.
- **Telegram's discretion:** Telegram "reserves the right to expand these terms and guidelines as the need arises" -- meaning the rules can change at any time.
- **Competitive response:** Telegram could incorporate your differentiating features into the official app, eliminating your value proposition.

### Legal Risks
- **GPL compliance:** Forking the official apps requires you to open-source your code. Any proprietary features visible in the fork must be published. Failure to comply exposes you to copyright claims.
- **Trademark issues:** Accidental or insufficient distancing from the "Telegram" brand can lead to trademark disputes.
- **Data protection:** You become a data processor for user communications, bringing GDPR/privacy regulation obligations.

### Operational Risks
- **Push notifications:** Require Firebase (Android) or APNs (iOS) setup with your own accounts. Misconfiguration means users don't get message notifications.
- **User trust:** Users must trust your app with their Telegram credentials. Any security incident destroys credibility.
- **Rate limiting:** Telegram applies strict rate limits that can affect your users if not carefully managed.

---

## Summary Assessment

Building a custom Telegram client is **technically feasible and explicitly supported by Telegram**. The two viable approaches are:

1. **Fork the official app** (faster, lower effort, must be GPL open source) -- best for adding features on top of the existing Telegram experience.
2. **Build from scratch on TDLib** (much more effort, can be proprietary via Boost license) -- best for a fundamentally different UX.

The **biggest ongoing costs** are upstream merge maintenance and staying compliant with evolving Telegram policies. The **biggest risks** are API access revocation at Telegram's discretion and app store removal. Multiple successful third-party clients (Nicegram, Nekogram, Plus Messenger) prove the model works, but all operate at the pleasure of Telegram's policy enforcement.

---

## Sources
- [Telegram-iOS Official Repo](https://github.com/TelegramMessenger/Telegram-iOS)
- [Telegram Android Official Repo](https://github.com/DrKLO/Telegram)
- [Telegram X Official Repo](https://github.com/TGX-Android/Telegram-X)
- [Telegram Desktop Official Repo](https://github.com/telegramdesktop)
- [TDLib Official Repo](https://github.com/tdlib/td)
- [TDLib Documentation](https://core.telegram.org/tdlib)
- [TDLib Blog Announcement](https://telegram.org/blog/tdlib)
- [Telegram API Terms of Service](https://core.telegram.org/api/terms)
- [Obtaining Telegram API ID](https://core.telegram.org/api/obtaining_api_id)
- [Telegram Applications Page](https://telegram.org/apps)
- [Telegram Reproducible Builds](https://core.telegram.org/reproducible-builds)
- [Nicegram Official Site](https://nicegram.app/)
- [Nicegram Android Repo](https://github.com/nicegram/nicegram-android)
- [Swiftgram Repo](https://github.com/Swiftgram/Telegram-iOS)
- [Nekogram Repo](https://github.com/Nekogram/Nekogram)
- [Telegram macOS Repo](https://github.com/overtake/TelegramSwift)
- [BetterTG - SwiftUI TDLib Client](https://github.com/levochkaa/BetterTG)
- [TDLib Ban Issues Discussion](https://github.com/tdlib/td/issues/534)
- [Telegram Source Code Analysis](https://typevar.dev/articles/DrKLO/Telegram)
