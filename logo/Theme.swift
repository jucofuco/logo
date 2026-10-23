import SwiftUI
import UIKit

// Copied from hardoff/snipoff (docs/design.md "Reusing it in another app"). Change the accent
// below if this app needs its own brand color; keep everything else.

/// Calm neutrals, one violet accent (same family as hardoff/snipoff). Every token has a light and
/// a dark value and follows the system appearance.
enum Theme {
    static let uiBackground = UIColor(light: 0xF5F4F1, dark: 0x0E0E10)
    static let uiCard = UIColor(light: 0xFFFFFF, dark: 0x1C1C1F)
    static let uiRaised = UIColor(light: 0xECEBE7, dark: 0x2A2A2E)
    static let uiStroke = UIColor(light: 0x000000, lightAlpha: 0.06, dark: 0xFFFFFF, darkAlpha: 0.07)
    static let uiText = UIColor(light: 0x1A1A1C, dark: 0xF4F3F0)
    static let uiMuted = UIColor(light: 0x6B6A70, dark: 0xA3A2A8)
    static let uiFaint = UIColor(light: 0xA09FA5, dark: 0x6A696F)
    static let uiAccent = UIColor(light: 0x6E56CF, dark: 0x9E8CFC)
    static let uiOnAccent = UIColor(light: 0xFFFFFF, dark: 0x16131F)
    static let uiShadow = UIColor(light: 0x000000, lightAlpha: 0.05, dark: 0x000000, darkAlpha: 0)

    static let background = Color(uiBackground)
    static let card = Color(uiCard)
    static let raised = Color(uiRaised)
    static let stroke = Color(uiStroke)
    static let text = Color(uiText)
    static let muted = Color(uiMuted)
    static let faint = Color(uiFaint)
    static let accent = Color(uiAccent)
    static let onAccent = Color(uiOnAccent)
    static let shadow = Color(uiShadow)
}

/// Light, dark, or follow the system. Picked in Settings, like hardoff/snipoff.
enum Appearance: String, CaseIterable, Identifiable {
    case system, light, dark

    var id: String { rawValue }
    var title: String { rawValue.capitalized }

    var colorScheme: ColorScheme? {
        switch self {
        case .system: nil
        case .light: .light
        case .dark: .dark
        }
    }
}

/// Applies the picked appearance. Needed on the root and on every sheet:
/// sheets are their own window and don't inherit it.
private struct FollowsAppearance: ViewModifier {
    @AppStorage("appearance") private var appearance = Appearance.system

    func body(content: Content) -> some View {
        content.preferredColorScheme(appearance.colorScheme)
    }
}

extension View {
    func followsAppearance() -> some View { modifier(FollowsAppearance()) }
}

extension UIColor {
    convenience init(light: UInt32, lightAlpha: CGFloat = 1, dark: UInt32, darkAlpha: CGFloat = 1) {
        self.init { traits in
            traits.userInterfaceStyle == .dark
                ? UIColor(hex: dark, alpha: darkAlpha)
                : UIColor(hex: light, alpha: lightAlpha)
        }
    }

    convenience init(hex: UInt32, alpha: CGFloat = 1) {
        self.init(
            red: CGFloat((hex >> 16) & 0xFF) / 255,
            green: CGFloat((hex >> 8) & 0xFF) / 255,
            blue: CGFloat(hex & 0xFF) / 255,
            alpha: alpha
        )
    }
}

extension Font {
    static func display(_ size: CGFloat, weight: Font.Weight = .bold) -> Font {
        .system(size: size, weight: weight, design: .rounded)
    }

    /// Small uppercase section labels.
    static let eyebrow = Font.system(size: 11, weight: .semibold, design: .rounded)
}

extension View {
    func card(padding: CGFloat = 18) -> some View {
        self
            .padding(padding)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background {
                // Shadow from the shape only, not from every text inside the card.
                RoundedRectangle(cornerRadius: 22, style: .continuous)
                    .fill(Theme.card)
                    .shadow(color: Theme.shadow, radius: 14, y: 4)
            }
            .overlay(
                RoundedRectangle(cornerRadius: 22, style: .continuous).stroke(Theme.stroke, lineWidth: 1)
            )
    }

    func eyebrow() -> some View {
        self.font(.eyebrow).tracking(1.4).textCase(.uppercase).foregroundStyle(Theme.muted)
    }
}
