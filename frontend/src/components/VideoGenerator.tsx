import React, { useState } from 'react'
import {
  Card,
  Button,
  message,
  Typography,
  Space,
  Row,
  Col,
  Progress,
  Alert,
  Select,
  Input,
  Divider,
} from 'antd'
import {
  VideoCameraOutlined,
  PlayCircleOutlined,
  DownloadOutlined,
  SettingOutlined,
} from '@ant-design/icons'
import { generateVideo, getGenerationStatus } from '../services/api'

const { Title, Paragraph } = Typography
const { Option } = Select
const { TextArea } = Input

interface VideoSettings {
  resolution: string
  fps: number
  duration: number
  quality: string
}

const VideoGenerator: React.FC = () => {
  const [scriptContent, setScriptContent] = useState('')
  const [characters] = useState<string[]>([])
  const [scenes] = useState<string[]>([])
  const [videoSettings, setVideoSettings] = useState<VideoSettings>({
    resolution: '1920x1080',
    fps: 24,
    duration: 30,
    quality: 'high',
  })
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [videoUrl, setVideoUrl] = useState<string | null>(null)
  const [, setTaskId] = useState<string | null>(null)

  const handleGenerateVideo = async () => {
    if (!scriptContent.trim()) {
      message.warning('请输入剧本内容')
      return
    }

    setLoading(true)
    setProgress(0)
    setVideoUrl(null)

    try {
      const scriptData = {
        script_text: scriptContent,
        characters: characters,
        scenes: scenes,
        settings: videoSettings,
      }

      const result = await generateVideo(scriptData)
      setTaskId(result.task_id)
      
      // 开始轮询状态
      pollGenerationStatus(result.task_id)
      
      message.success('视频生成任务已启动！')
    } catch (error) {
      console.error('生成视频失败:', error)
      message.error('生成视频失败，请重试')
      setLoading(false)
    }
  }

  const pollGenerationStatus = async (taskId: string) => {
    const pollInterval = setInterval(async () => {
      try {
        const status = await getGenerationStatus(taskId)
        
        if (status.progress !== undefined) {
          setProgress(status.progress)
        }
        
        if (status.status === 'completed') {
          clearInterval(pollInterval)
          setLoading(false)
          setVideoUrl(status.video_url)
          setProgress(100)
          message.success('视频生成完成！')
        } else if (status.status === 'failed') {
          clearInterval(pollInterval)
          setLoading(false)
          message.error('视频生成失败：' + (status.error || '未知错误'))
        }
      } catch (error) {
        console.error('获取生成状态失败:', error)
      }
    }, 2000) // 每2秒检查一次状态
  }

  const handleDownloadVideo = () => {
    if (videoUrl) {
      const link = document.createElement('a')
      link.href = videoUrl
      link.download = 'generated_video.mp4'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
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
李明：因为面对你，我总是词穷，只能说最真实的感受。`

  return (
    <div>
      <Title level={2}>
        <VideoCameraOutlined /> 视频生成
      </Title>

      <Row gutter={[24, 24]}>
        <Col xs={24} lg={16}>
          <Card title="剧本内容">
            <Space direction="vertical" style={{ width: '100%' }}>
              <TextArea
                value={scriptContent}
                onChange={(e) => setScriptContent(e.target.value)}
                placeholder={`请输入完整的剧本内容，包括角色、场景和对话\n\n示例：\n${sampleScript}`}
                rows={12}
              />
              
              <Button
                type="link"
                onClick={() => setScriptContent(sampleScript)}
              >
                使用示例剧本
              </Button>
            </Space>
          </Card>

          {loading && (
            <Card title="生成进度" style={{ marginTop: 24 }}>
              <Space direction="vertical" style={{ width: '100%' }}>
                <Progress percent={progress} status={progress === 100 ? 'success' : 'active'} />
                <Paragraph type="secondary">
                  {progress < 25 && '正在解析剧本...'}
                  {progress >= 25 && progress < 50 && '正在生成角色和场景...'}
                  {progress >= 50 && progress < 75 && '正在生成视频帧...'}
                  {progress >= 75 && progress < 100 && '正在合成最终视频...'}
                  {progress === 100 && '视频生成完成！'}
                </Paragraph>
              </Space>
            </Card>
          )}

          {videoUrl && (
            <Card title="生成结果" style={{ marginTop: 24 }}>
              <Space direction="vertical" style={{ width: '100%' }}>
                <video
                  controls
                  style={{ width: '100%', maxHeight: '400px' }}
                  src={videoUrl}
                >
                  您的浏览器不支持视频播放。
                </video>
                
                <Space>
                  <Button
                    type="primary"
                    icon={<DownloadOutlined />}
                    onClick={handleDownloadVideo}
                  >
                    下载视频
                  </Button>
                  
                  <Button
                    icon={<PlayCircleOutlined />}
                    onClick={() => window.open(videoUrl, '_blank')}
                  >
                    在新窗口播放
                  </Button>
                </Space>
              </Space>
            </Card>
          )}
        </Col>

        <Col xs={24} lg={8}>
          <Card title="视频设置" extra={<SettingOutlined />}>
            <Space direction="vertical" style={{ width: '100%' }}>
              <div>
                <Paragraph>分辨率</Paragraph>
                <Select
                  value={videoSettings.resolution}
                  onChange={(value) => setVideoSettings({ ...videoSettings, resolution: value })}
                  style={{ width: '100%' }}
                >
                  <Option value="1920x1080">1920x1080 (Full HD)</Option>
                  <Option value="1280x720">1280x720 (HD)</Option>
                  <Option value="854x480">854x480 (SD)</Option>
                </Select>
              </div>

              <div>
                <Paragraph>帧率 (FPS)</Paragraph>
                <Select
                  value={videoSettings.fps}
                  onChange={(value) => setVideoSettings({ ...videoSettings, fps: value })}
                  style={{ width: '100%' }}
                >
                  <Option value={24}>24 FPS</Option>
                  <Option value={30}>30 FPS</Option>
                  <Option value={60}>60 FPS</Option>
                </Select>
              </div>

              <div>
                <Paragraph>视频时长 (秒)</Paragraph>
                <Select
                  value={videoSettings.duration}
                  onChange={(value) => setVideoSettings({ ...videoSettings, duration: value })}
                  style={{ width: '100%' }}
                >
                  <Option value={15}>15秒</Option>
                  <Option value={30}>30秒</Option>
                  <Option value={60}>1分钟</Option>
                  <Option value={120}>2分钟</Option>
                </Select>
              </div>

              <div>
                <Paragraph>视频质量</Paragraph>
                <Select
                  value={videoSettings.quality}
                  onChange={(value) => setVideoSettings({ ...videoSettings, quality: value })}
                  style={{ width: '100%' }}
                >
                  <Option value="high">高质量</Option>
                  <Option value="medium">中等质量</Option>
                  <Option value="low">低质量</Option>
                </Select>
              </div>

              <Divider />

              <Button
                type="primary"
                size="large"
                block
                loading={loading}
                onClick={handleGenerateVideo}
                disabled={!scriptContent.trim()}
              >
                {loading ? '生成中...' : '开始生成视频'}
              </Button>
            </Space>
          </Card>

          <Card title="使用说明" style={{ marginTop: 24 }}>
            <Space direction="vertical">
              <Alert
                message="生成提示"
                description="视频生成可能需要几分钟时间，请耐心等待。生成过程中请不要关闭页面。"
                type="info"
                showIcon
              />
              
              <div>
                <Paragraph strong>剧本格式要求：</Paragraph>
                <ul style={{ paddingLeft: '20px' }}>
                  <li>包含标题、角色描述</li>
                  <li>明确的场景设置</li>
                  <li>清晰的对话内容</li>
                  <li>角色和场景描述要详细</li>
                </ul>
              </div>
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default VideoGenerator