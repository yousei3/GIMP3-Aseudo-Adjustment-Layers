# Pseudo Adjustment Layer for GIMP 3

**Pseudo Adjustment Layer** is a Python plug-in that leverages the new Non-Destructive Editing (NDE) features in GIMP 3.0/3.2 to simulate "Adjustment Layers", a familiar and essential feature in image editors like Photoshop.

It allows you to easily add, manage, and re-edit non-destructive filters from a dedicated palette without directly altering the original pixels of your image.

## ✨ Key Features

* **Automatic Pseudo Adjustment Layer Generation**: Selecting a filter automatically creates a Layer Group with a transparent dummy layer inside, and applies the non-destructive filter to the group itself.
* **Automatic Selection Masking**: If a selection exists when applying a filter, it is automatically converted into a Layer Mask for the group.
* **Perfect Match with GIMP Menus**: Displays over 100 GEGL filters in the exact same categories and order as GIMP's official `Filters` menu.
* **Powerful Management Tools**: 
    * 🔍 Real-time incremental search.
    * ⭐ Favorites system (right-click to add/remove).
    * 📝 History of recently used filters (up to 10).
    * 📂 Clean, accordion-style exclusive folder expansion.
* **Fully Customisable Multilingual Support**: When you select a language in the plug-in, a JSON file for that language is automatically generated in the `Language` folder. You can freely change any UI display names by editing this file.
* **Safe Validation**: Clicking the **`Reset List`** button at the bottom of the palette not only reloads the list but also automatically tests internal GEGL nodes. It safely excludes any nodes that do not function correctly as non-destructive filters.

## ⚙️ How it Works

In the current specification of GIMP 3, it is not possible to apply a filter directly to an empty layer.
This plug-in achieves the behaviour of an adjustment layer by executing the following steps instantly in the background:

1. Creates a new Layer Group (named `fx: Filter Name`) directly above the currently selected layer.
2. Places a transparent layer (named `DUMMY`) inside the group.
3. Adds a Layer Mask to the group (if a selection is active).
4. Applies the specified non-destructive filter to the Layer Group itself.

This workflow allows you to adjust parameters, toggle visibility, or repaint the mask at any time later.

## 📦 Installation

1. Download and extract `pseudo_adjustment_layers.zip`.
2. Place the extracted folder in your GIMP 3 plug-ins directory:
   * **Linux**: `~/.config/GIMP/3.0/plug-ins/`
   * **Windows**: `C:\Users\[Username]\AppData\Roaming\GIMP\3.0\plug-ins\`

   Make sure the folder structure looks like this:

       plug-ins/
          └── pseudo_adjustment_layers/
                   └── pseudo_adjustment_layers.py

3. Grant execution permissions to the file.
   * On Linux, run: `chmod +x pseudo_adjustment_layers.py` in your terminal.
4. Restart GIMP.

## 🚀 Usage

1. Launch the palette from the GIMP menu: **`Filters` > `Pseudo Adjustment Layer`**. (The palette stays on top of the GIMP window).
   > **NOTE**: On first startup, please click the **`🔄 Reset List`** button at the bottom of the palette to initialize the filter list.
2. Select the target layer in your image to which you want to apply the filter.
3. **Double-click** (or press Enter on) a filter name in the palette to apply it as a pseudo adjustment layer above the selected layer.

### Customising the UI
When you choose a language via the `🌐 Select` button, a `Language` folder is created next to the plug-in, containing a `(language_code).json` file (e.g., `ja.json` or `en_GB.json`).
By opening this JSON file in a text editor and modifying the `"local"` values, you can customise the category and filter names displayed in the palette to your liking. After editing, click the button at the bottom of the palette to validate and reload your custom translations.

## ⚠️ Requirements
* GIMP 3.0 or 3.2+
* Python 3 environment with GObject Introspection (GIR) support

## 📜 License
This project is open source and available under the [GNU General Public License v3.0 (GPLv3)](LICENSE).

# Pseudo Adjustment Layer for GIMP 3

**Pseudo Adjustment Layer** は、GIMP 3.0/3.2 の新しい非破壊編集（NDE）機能を活用し、Photoshopなどの画像編集ソフトでお馴染みの「調整レイヤー（Adjustment Layers）」を擬似的に実現するPythonプラグインです。

画像の元のピクセルを直接書き換えることなく、専用のパレットから手軽に非破壊フィルタを追加・管理・再編集することができます。

## ✨ 主な特徴

* **擬似・調整レイヤーの自動生成**: フィルタを選択すると、自動的にレイヤーグループと透明なダミーレイヤーを生成し、グループに対して非破壊フィルタを適用します。
* **選択範囲の自動マスク化**: 選択範囲が存在した状態でフィルタを適用すると、自動的にレイヤーグループのマスクへと変換されます。
* **GIMP公式メニューと完全一致**: 100種類以上のGEGLフィルタを、GIMP公式の `Filters` メニューと全く同じカテゴリ・並び順で美しく表示します。
* **強力な管理機能**: 
    * 🔍 リアルタイムのインクリメンタル検索
    * ⭐ お気に入り機能（右クリックで登録）
    * 📝 最近使ったフィルタの履歴保存（最大10件）
    * 📂 見やすい排他的（アコーディオン式）なフォルダ展開
* **フルカスタマイズ可能な多言語対応**: プラグイン上で言語を選択すると、自動的に `Language` フォルダに各言語用のJSONファイルが生成されます。ユーザー自身でこの翻訳ファイルを書き換えることで、UIの表示名を完全に自由に変更できます。
* **安全なバリデーション機能**: パレット下部の「Reset List」ボタンを押すと、リストの初期化と同時に、非破壊フィルタとして正常に動作しない（適用するとエラーになる）内部用のGEGLノードを自動でテストし、リストから安全に除外します。

## ⚙️ 仕組み

GIMP 3の現在の仕様では、何もない空のレイヤーに直接フィルタをかけることはできません。
このプラグインは、以下の手順をバックグラウンドで瞬時に実行することで、調整レイヤーのような振る舞いを実現しています。

1. 選択中のレイヤーの上に新しい「レイヤーグループ（`fx: フィルタ名`）」を作成。
2. グループの中に、透明で塗りつぶされた「ダミーレイヤー（`DUMMY`）」を配置。
3. （選択範囲があれば）グループに対してレイヤーマスクを追加。
4. グループ自体に対して、指定された非破壊フィルタを適用。

これにより、後からいつでもパラメータを調整したり、フィルタの表示/非表示を切り替えたり、マスクを描き直したりすることが可能になります。

## 📦 インストール方法

1. `pseudo_adjustment_layers.zip` をダウンロードして解凍します。
2. GIMP 3 のプラグインフォルダに配置します。
   * **Linux**: `~/.config/GIMP/3.0/plug-ins/`
   * **Windows**: `C:\Users\[ユーザー名]\AppData\Roaming\GIMP\3.0\plug-ins\`
   
   以下のようなフォルダ構造になるように配置してください。

       plug-ins/
          └── pseudo_adjustment_layers/
                   └── pseudo_adjustment_layers.py

3. 配置したファイルに実行権限を付与します。
   * Linuxの場合: 端末で `chmod +x pseudo_adjustment_layers.py` を実行してください。
4. GIMPを再起動します。

## 🚀 使い方

1. GIMPのメニューから **`Filters` > `Pseudo Adjustment Layer`** を選択してパレットを起動します。（パレットは常に最前面に表示されます）
   > **NOTE**: 初回起動時はパレット下部の **`🔄 Reset List`** ボタンを押してリストを初期化してください。
2. フィルタを適用したい対象のレイヤーを選択します。
3. パレット内のフィルタ名を**ダブルクリック**（またはEnterキー）すると、擬似的な調整レイヤーとして対象レイヤーの上に適用されます。

### UIのカスタマイズについて
パレット上部の `🌐 Select` ボタンから言語を選ぶと、プラグインと同じディレクトリに `Language` フォルダが作成され、その中に `(言語コード).json` （例: `ja.json`）が生成されます。
このJSONファイルをテキストエディタで開き、`"local"` の値を書き換えることで、パレットに表示されるカテゴリ名やフィルタ名を自分好みにカスタマイズできます。書き換えた後は、パレット下部のボタンを押すことで、バリデーションと共に最新の翻訳データが再読み込みされます。

## ⚠️ 必須要件
* GIMP 3.0 または 3.2 以上
* GObject Introspection (GIR) 対応のPython 3環境

## 📜 ライセンス
このプロジェクトはオープンソースであり、[GNU General Public License v3.0 (GPLv3)](LICENSE) の下で利用可能です。
