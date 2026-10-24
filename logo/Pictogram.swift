import SwiftUI
import UIKit

/// Which set of pictures the cards show. The files are `Pictograms/<folder>/<word id>.png` in the app
/// (made by `pictograms/export_png.py`). Without a file for a word the card shows its emoji.
enum PictureStyle: Int, CaseIterable, Identifiable {
    case v1 = 1, v2, mulberry

    var id: Int { rawValue }

    var folder: String {
        switch self {
        case .v1: "v1"
        case .v2: "v2"
        case .mulberry: "mulberry"
        }
    }

    var title: String {
        switch self {
        case .v1: "Style 1"
        case .v2: "Style 2"
        case .mulberry: "Mulberry"
        }
    }

    var note: String {
        switch self {
        case .v1: "Our first drawings."
        case .v2: "Thinner lines, calmer faces."
        case .mulberry: "Symbols by Steve Lee, Mulberry Symbols, CC BY-SA 4.0 (mulberrysymbols.org). Words without a Mulberry symbol use our own drawing."
        }
    }
}

/// Loads pictogram files once and keeps them.
@MainActor
final class PictogramCache {
    static let shared = PictogramCache()

    private var images: [String: UIImage] = [:]
    private var missing: Set<String> = []

    func image(_ id: String, style: PictureStyle) -> UIImage? {
        let key = "\(style.folder)/\(id)"
        if let image = images[key] { return image }
        if missing.contains(key) { return nil }
        guard let path = Bundle.main.path(forResource: id, ofType: "png", inDirectory: "Pictograms/\(style.folder)"),
              let image = UIImage(contentsOfFile: path) else {
            missing.insert(key)
            return nil
        }
        images[key] = image
        return image
    }
}

/// The pictogram of a word (or a folder icon), or its emoji if there is none in the picked set.
struct Pictogram: View {
    let id: String?
    let fallback: String
    @AppStorage("pictureStyle") private var style = PictureStyle.v1

    var body: some View {
        if let id, let image = PictogramCache.shared.image(id, style: style) {
            Image(uiImage: image)
                .resizable()
                .scaledToFit()
                .accessibilityHidden(true)
        } else {
            Text(fallback)
                .font(.system(size: 40))
                .minimumScaleFactor(0.3)
                .accessibilityHidden(true)
        }
    }
}
