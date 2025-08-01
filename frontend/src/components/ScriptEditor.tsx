import React, { useState } from 'react'
import { Card, Input, Button, message, Typography, Space, Divider } from 'antd'
import { FileTextOutlined, SendOutlined } from '@ant-design/icons'
import { parseScript } from '../services/api'

const { TextArea } = Input
const { Title, Paragraph } = Typography

interface ParsedScript {
  title: string
  characters: Array<{
    name: string
    description: string
  }>
  scenes: Array<{
    description: string
    dialogues: Array<{
      character: string
      text: string
    }>
  }>
}

const ScriptEditor: React.FC = () => {
  const [scriptText, setScriptText] = useState('')
  const [parsedScript, setParsedScript] = useState<ParsedScript | null>(null)
  const [loading, setLoading] = useState(false)

  const handleParseScript = async () => {
    if (!scriptText.trim()) {
      message.warning('请输入剧本内容')
      return
    }

    setLoading(true)
    try {
      const result = await parseScript(scriptText)
      setParsedScript(result)
      message.success('剧本解析成功！')
    } catch (error) {
      console.error('解析剧本失败:', error)
      message.error('解析剧本失败，请检查剧本格式')
    } finally {
      setLoading(false)
    }
  }

  const sampleScript = `标题：浪漫晚餐

场景：温馨的餐厅
时间：晚上
氛围：浪漫、温馨

角色：
- 李明：25岁男性，温文尔雅，穿着白色衬衫
- 小雅：23岁女性，甜美可爱，穿着粉色连衣裙

第一场：
李明：今晚的月色真美，就像你一样。
小雅：你总是这么会说话。
李明：因为面对你，我总是词穷，只能说最真实的感受。

第二场：
小雅：这家餐厅的环境真不错。
李明：我特意挑选的，希望你喜欢。
小雅：我很喜欢，谢谢你的用心。`

  return (
    <div>
      <Title level={2}>
        <FileTextOutlined /> 剧本编辑
      </Title>
      
      <Card title="剧本输入" style={{ marginBottom: 24 }}>
        <Space direction="vertical" style={{ width: '100%' }}>
          <Paragraph>
            请输入您的剧本内容，系统将自动解析角色、场景和对话信息。
          </Paragraph>
          
          <TextArea
            value={scriptText}
            onChange={(e) => setScriptText(e.target.value)}
            placeholder={`请输入剧本内容，格式示例：\n\n${sampleScript}`}
            rows={12}
            className="script-editor"
          />
          
          <Button
            type="primary"
            icon={<SendOutlined />}
            onClick={handleParseScript}
            loading={loading}
            size="large"
          >
            解析剧本
          </Button>
        </Space>
      </Card>

      {parsedScript && (
        <Card title="解析结果">
          <Space direction="vertical" style={{ width: '100%' }}>
            <div>
              <Title level={4}>剧本标题</Title>
              <Paragraph>{parsedScript.title}</Paragraph>
            </div>
            
            <Divider />
            
            <div>
              <Title level={4}>角色列表</Title>
              {parsedScript.characters.map((character, index) => (
                <Card key={index} size="small" style={{ marginBottom: 8 }}>
                  <Paragraph>
                    <strong>{character.name}:</strong> {character.description}
                  </Paragraph>
                </Card>
              ))}
            </div>
            
            <Divider />
            
            <div>
              <Title level={4}>场景和对话</Title>
              {parsedScript.scenes.map((scene, sceneIndex) => (
                <Card key={sceneIndex} size="small" style={{ marginBottom: 16 }}>
                  <Title level={5}>场景 {sceneIndex + 1}</Title>
                  <Paragraph>{scene.description}</Paragraph>
                  
                  {scene.dialogues.map((dialogue, dialogueIndex) => (
                    <div key={dialogueIndex} style={{ marginBottom: 8 }}>
                      <Paragraph>
                        <strong>{dialogue.character}:</strong> {dialogue.text}
                      </Paragraph>
                    </div>
                  ))}
                </Card>
              ))}
            </div>
          </Space>
        </Card>
      )}
    </div>
  )
}

export default ScriptEditor