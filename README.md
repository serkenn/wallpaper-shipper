# wallpaper-shipper

`images/` に画像を置いて `main` へ push すると、GitHub Actions が `metadata/wallpapers.csv` を自動同期します。

## フロー

1. 画像を追加して push
2. Actions が `metadata/wallpapers.csv` を作成/更新（`tier` と `Type` は空欄）
3. `tier` と `Type` を埋めて再度 push
4. Actions が検証後、画像 + CSV を同梱した zip を GitHub Release に作成

## ディレクトリ

- `images/`: 配布したい画像ファイル
- `metadata/wallpapers.csv`: 画像メタデータ (`filename,tier,Type`)
- `.github/workflows/wallpaper-release.yml`: 自動化ワークフロー
- `scripts/sync_csv.py`: 画像一覧とCSV同期
- `scripts/check_release_ready.py`: Release可否の検証

## 注意

- `filename` は画像ファイル名と一致させてください。
- `tier` または `Type` が1つでも空欄なら、Release作成はスキップされます。
