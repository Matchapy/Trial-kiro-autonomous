# AWS re:Invent 2025 プレゼンテーション資料

このリポジトリには、AWS re:Invent 2025で発表された新サービスに関する包括的なプレゼンテーション資料が含まれています。

## 📚 資料構成

### マスターカタログ
- **[AWS_re_Invent_2025_サービスカタログ.md](AWS_re_Invent_2025_サービスカタログ.md)**
  - すべての新サービスをカテゴリ別に整理したマスターカタログ
  - 各サービスの簡潔な説明（日本語）
  - カテゴリ: AI/機械学習、モダナイゼーション、ネットワーキング、セキュリティ、カスタマーサービス、データベース、オブザーバビリティ、マーケットプレイス

### 個別サービスプレゼンテーション（presentations/）

各サービスの詳細なプレゼンテーション資料が用意されています。

#### AI/機械学習
1. **[Amazon Nova 2 Lite](presentations/01_Amazon_Nova_2_Lite.md)**
   - 高速・低コストの軽量AIモデル
   - 基本的な推論タスクに最適

2. **[Amazon Nova 2 Pro](presentations/02_Amazon_Nova_2_Pro.md)**
   - 高度な推論能力を持つプロフェッショナル向けモデル
   - エンタープライズレベルのAI活用

3. **[Amazon Nova 2 Sonic](presentations/03_Amazon_Nova_2_Sonic.md)**
   - スピーチ・ツー・スピーチモデル
   - 自然でリアルタイムの会話型AI

4. **[Amazon Nova 2 Omni](presentations/04_Amazon_Nova_2_Omni.md)**
   - マルチモーダル対応の汎用AIモデル
   - テキスト、画像、音声の統合処理

5. **[Trainium3 チップ](presentations/05_Trainium3_Chip.md)**
   - 第4世代AI専用チップ
   - 4倍の処理速度、50%のコスト削減

6. **[Frontier Agents](presentations/06_Frontier_Agents.md)**
   - 自律的に動作する次世代AIエージェント
   - Kiro、Security、DevOpsの3つのエージェント

7. **[Amazon Bedrock Open Training](presentations/07_Amazon_Bedrock_Open_Training.md)**
   - カスタムモデル開発サービス
   - Novaモデルをベースにした独自モデル構築

#### モダナイゼーション
8. **[AWS Transform](presentations/08_AWS_Transform.md)**
   - レガシーシステムのモダナイゼーション
   - メインフレーム、Windows、カスタムシステム対応

#### ネットワーキング
9. **[マルチクラウドネットワーキング](presentations/09_Multi_Cloud_Networking.md)**
   - AWSとGoogle Cloudの統一仕様
   - シームレスなマルチクラウド接続

#### セキュリティ
10. **[IAM Access Analyzer 内部アクセス分析](presentations/10_IAM_Access_Analyzer_Enhancements.md)**
    - 組織内アクセスの可視化
    - 自動推論による分析

11. **[IAM MFA 強制適用](presentations/11_IAM_MFA_Enforcement.md)**
    - 100% MFAカバレッジ達成
    - パスワード攻撃の99%以上を防止

#### カスタマーサービス
12. **[Amazon Connect AI 機能強化](presentations/12_Amazon_Connect_AI.md)**
    - 29の新しいエージェント型AI機能
    - 超人的な能力をエージェントに提供

#### データベース
13. **[データベースサービス強化](presentations/13_Database_Services.md)**
    - Amazon RDSとDynamoDBの改善
    - パフォーマンスと可観測性の向上

#### オブザーバビリティ
14. **[CloudWatch 生成AIオブザーバビリティ](presentations/14_CloudWatch_AI_Observability.md)**
    - AIアプリケーションの包括的監視
    - AgentCoreとの統合

#### マーケットプレイス
15. **[AWS Marketplace 拡張機能](presentations/15_AWS_Marketplace_Enhancements.md)**
    - AI検索、自動価格設定
    - マルチプロダクトソリューション

## 🎯 使用方法

### プレゼンテーション用
1. マスターカタログで全体像を把握
2. 各サービスの個別資料で詳細を説明
3. Markdownファイルをそのまま表示、またはPDF/PowerPointに変換

### 学習・研究用
- 各資料には以下の情報が含まれています：
  - サービス概要
  - 主な機能と特徴
  - パフォーマンスメトリクス
  - ユースケースとメリット
  - 技術仕様
  - ベストプラクティス

### 変換方法
Markdownファイルを他の形式に変換する場合：

```bash
# Pandocを使用してPDFに変換
pandoc AWS_re_Invent_2025_サービスカタログ.md -o output.pdf

# PowerPointに変換
pandoc presentations/01_Amazon_Nova_2_Lite.md -o output.pptx
```

## 📊 主要統計

### AI/機械学習
- **Nova 2**: 4つの新モデル（Lite, Pro, Sonic, Omni）
- **Trainium3**: 前世代比4倍の性能、50%のコスト削減
- **Frontier Agents**: 数時間〜数日間の自律動作

### モダナイゼーション
- **分析コード**: 11億行以上
- **削減工数**: 81万時間以上
- **速度向上**: 4〜5倍
- **コスト削減**: 最大70%

### セキュリティ
- **MFAカバレッジ**: 100%達成（業界初）
- **攻撃防止率**: 99%以上

### カスタマーサービス
- **新機能**: 29のエージェント型AI機能
- **対応言語**: 30以上

## 🔄 更新履歴

- **2025-12-03**: 初版作成
  - AWS re:Invent 2025で発表された全15サービスの資料を作成
  - マスターカタログを作成

## 📝 ライセンス

本資料は、AWS re:Invent 2025の公開情報に基づいて作成されています。

## 🤝 貢献

この資料に追加情報や修正がある場合は、プルリクエストを送信してください。

## 📧 お問い合わせ

ご質問やフィードバックがありましたら、Issueを作成してください。

---

**作成日**: 2025年12月3日  
**イベント**: AWS re:Invent 2025  
**場所**: ラスベガス、ネバダ州  
**開催期間**: 2025年12月1日〜5日
