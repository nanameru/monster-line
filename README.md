# monster-line

Claude Code のステータスラインに住むモンスターを育てよう。

Claude Code を使えば使うほど経験値が溜まり、モンスターが進化していきます。

## 進化の流れ

```
( ○ )  →  ^(◕‿◕)^  →  ∧(・ω・)∧  →  }(▼皿▼){  →  竜(◇ᴗ◇)彡  →  ✦(≖ᴗ≖)✦
タマゴ     スライム       ウルフ        アクマ        リュウ       シンリュウ
```

## セットアップ

```bash
git clone https://github.com/yourname/monster-line.git
cd monster-line
bash setup.sh
```

Claude Code を再起動すればモンスターが現れます。

## 仕組み

- ステータスラインが更新されるたびにモンスターがアニメーションします
- 5分ごとに経験値 +15
- 経験値が一定に達すると次のステージに進化
- セーブデータは `~/.claude/monster/save.json` に保存

## 進化テーブル

| ステージ | 名前 | 必要XP |
|---------|------|--------|
| 1 | タマゴ | 0 |
| 2 | スライム | 100 |
| 3 | ウルフ | 400 |
| 4 | アクマ | 1000 |
| 5 | リュウ | 2500 |
| 6 | シンリュウ | 6000 |

## アンインストール

`~/.claude/settings.json` から `statusLine` の設定を削除し、`~/.claude/monster.sh` と `~/.claude/monster/` を削除してください。

## ライセンス

MIT
