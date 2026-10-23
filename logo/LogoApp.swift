import SwiftUI

@main
struct LogoApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .tint(Theme.accent)
                .followsAppearance()
        }
    }
}
