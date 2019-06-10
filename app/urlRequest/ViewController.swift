//
//  ViewController.swift
//  urlRequest
//
//  Created by Haotian Zhu on 22/5/19.
//  Copyright © 2019 Haotian Zhu. All rights reserved.
//

import UIKit
import AVKit
import Vision
import SwiftyJSON

struct Message: Decodable{
    
    let timestamp: String
    let className: String?
    let classProb: String?
    let info: String?
    let boxes: Array<Array<Float>>?
    
}

struct Connection: Decodable {
    let timestamp: String
    let connection: String
}

var receivedData: Message!
var mushwiki: JSON!


class ViewController: UIViewController, UINavigationControllerDelegate,  UIImagePickerControllerDelegate, AVCaptureVideoDataOutputSampleBufferDelegate {
    
    
    
//    @IBOutlet weak var activityIndicator: UIActivityIndicatorView!
    @IBOutlet weak var label: UILabel!
    @IBOutlet weak var confidence: UILabel!
    @IBOutlet weak var imageView: UIImageView!
    var predictImage: UIImage!
//    var labelInfo: String?
//    var predictConfidence: String!
    var httpResponse: Int = 0
    var activityIndicator: UIActivityIndicatorView = UIActivityIndicatorView()
    @IBOutlet weak var readMore: UIButton!
    let model = ImageClassifier()
    var localModel = false
    
    
    
    override func viewDidLoad() {
        
        super.viewDidLoad()
        activityIndicator.center = self.view.center
        activityIndicator.hidesWhenStopped = true
        activityIndicator.style = UIActivityIndicatorView.Style.whiteLarge
        view.addSubview(activityIndicator)
        print(httpResponse)
        readMore.isHidden = true
//        confidence.isHidden = true
        
        let path = Bundle.main.path(forResource:"data", ofType:"json")
        let text = try! String(contentsOfFile:path!, encoding: String.Encoding.utf8)
        let data = text.data(using: .utf8)
        
        mushwiki = try? JSON(data: data!)
    }
    
    
    @IBAction func getRequest(_ sender: Any) {
        
        localModel = !localModel
        if localModel{
            confidence.isHidden = false
            readMore.isHidden = true
            let captureSession = AVCaptureSession()
            captureSession.sessionPreset = .photo
            //
            guard let captureDevice = AVCaptureDevice.default(for: .video) else{return}
            
            guard let input = try? AVCaptureDeviceInput(device: captureDevice) else{return}
            captureSession.addInput(input)
            
            captureSession.startRunning()
            
            let previewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
            previewLayer.frame = CGRect(x: 0, y: 0, width: 350, height: 467)
            imageView.layer.addSublayer(previewLayer)
            let dataOutput = AVCaptureVideoDataOutput()
            dataOutput.setSampleBufferDelegate(self, queue: DispatchQueue(label: "videoQueue"))
            captureSession.addOutput(dataOutput)
        }
        else{
            confidence.isHidden = true
            imageView.layer.sublayers = nil
            DispatchQueue.main.async {
                self.label.text = "Select a mode"
            }
        }
        
        
    }
    
    func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        
        guard let pixelBuffer: CVPixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else{return}
        
        
        guard let model = try? VNCoreMLModel(for: ImageClassifier().model) else {return}
        let request = VNCoreMLRequest(model: model){
            (finishReq, err)in
            
            guard let results = finishReq.results as? [VNClassificationObservation] else{return}
            guard let firstObeservation = results.first else{return}
            
            print(firstObeservation.identifier, firstObeservation.confidence)
            DispatchQueue.main.async() {
                if(firstObeservation.confidence >= 0.6){
                    self.label.text = firstObeservation.identifier
                    let confidence = String(format: "Confidence: %.2f", firstObeservation.confidence*100)
                    self.confidence.text = "\(confidence)%"
                }
            }
            
        }
        
        try? VNImageRequestHandler(cvPixelBuffer: pixelBuffer, options: [:]).perform([request])
        
    }

    
    
    func encodeImage()-> Data{
        var processedImage: UIImage!
        let width = predictImage.size.width
        let height = predictImage.size.height
        if width > height{
             processedImage = predictImage.imageRotatedByDegrees(degrees: 270)
        }
        else{
            processedImage = predictImage
        }
        let imageData = processedImage.pngData()
        let encodeing = imageData?.base64EncodedData()
        return encodeing!
    }
    
    func handleBoxes(boundaries: Array<Array<Float>>){
        
        let displayHeight = 350 * predictImage.size.height / predictImage.size.width
        let widthRatio = 350/self.predictImage.size.width
        let heightRatio = displayHeight / predictImage.size.height
        let position_y = (467 - displayHeight)/2
        
        for boundary in boundaries{
            let redView: UIView = UIView()
            redView.backgroundColor = .red
            let x = CGFloat(boundary[0])*widthRatio
            let y = (CGFloat(boundary[1]) * heightRatio) + position_y
            let width = CGFloat(boundary[2]) * widthRatio
            let height = CGFloat(boundary[3]) * heightRatio
            redView.frame = CGRect(x: x, y: y, width: width, height: height)
            redView.alpha = 0.4
            self.imageView.addSubview(redView)
        }
    }
    
    
    func removeSubViews(){
        for view in imageView.subviews{
            view.removeFromSuperview()
        }
    }
        
    
    
    @IBAction func photoSource(_ sender: Any) {
        if localModel{
            localModel = false
            imageView.layer.sublayers = nil
            DispatchQueue.main.async {
                self.label.text = "Select a mode"
            }
        }
        readMore.isHidden = true
        confidence.isHidden = true
        httpResponse = 0
        print("photo button")
        let cloudImagePickerController = UIImagePickerController()
        cloudImagePickerController.delegate = self
        
        let actionSheet = UIAlertController(title: "Photo source", message: "Select photo from", preferredStyle: .actionSheet)
        
        actionSheet.addAction(UIAlertAction(title: "Camera", style: .default, handler: { (UIAlertAction) in
            
            if UIImagePickerController.isSourceTypeAvailable(.camera){
                
                cloudImagePickerController.sourceType = .camera
                self.present(cloudImagePickerController, animated: true, completion: nil)
                
            }else{
                
                print("Camera is not available")
        
            }
            
        }))
        
        actionSheet.addAction(UIAlertAction(title: "Image Library", style: .default, handler: { (UIAlertAction) in
            
            cloudImagePickerController.sourceType = .photoLibrary
            self.present(cloudImagePickerController, animated: true, completion: nil)
//            self.remoteIdentify()
        }))
        
        actionSheet.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: nil))
        
        self.present(actionSheet, animated: true, completion: nil)
        
    }
    
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        self.removeSubViews()
//        let image = info[UIImagePickerController.InfoKey.originalImage] as! UIImage
        do{
        let image = info[UIImagePickerController.InfoKey.originalImage]
        self.predictImage = image as? UIImage
        imageView.image = image as? UIImage
        picker.dismiss(animated: true, completion: nil)
        self.remoteIdentify()
        }catch{
            return
        }
    }
    
    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        picker.dismiss(animated: true, completion: nil)
    }
    
    func myGETRequest(completion: @escaping (_ json: Any?, _ error: Error?)->()){
        guard let url = URL(string: "http://35.201.9.84/") else {return}
        let session = URLSession.shared
        session.dataTask(with: url) { (data, response, error) in
            
            if let response = response{
                let httpStatus = response as? HTTPURLResponse
                self.httpResponse = httpStatus!.statusCode
                print(httpStatus!.statusCode)
               
            }
            
            if let data = data{
                do{
                    
                    let connection = try JSONDecoder().decode(Connection.self, from: data)

                    completion(connection, error)
                    
                } catch{
                    print(error)
                }
                
            }
            
            }.resume()
    }
    
    
    func myPOSTRequest(completion: @escaping (_ json: Any?, _ error: Error?)->()){
        label.text = "Please wait..."
        let output = encodeImage()
        guard let url = URL(string: "http://35.201.9.84/predict") else {return}
        var request = URLRequest(url: url)
        request.addValue("image/jpeg", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "POST"
        request.httpBody = output
        let session = URLSession.shared
        session.dataTask(with: request){
            (data, response, error) in
            if let response = response{

                let httpStatus = response as? HTTPURLResponse
                self.httpResponse = httpStatus!.statusCode
                print(httpStatus!.statusCode)
            }
            
            if let data = data{
                do{
                    let json = try JSONDecoder().decode(Message.self, from: data)
                    completion(json, error)
                    
                } catch{
                    print(error)
                }
            }
            }.resume()
        
    }
    
    func remoteIdentify(){
        activityIndicator.startAnimating()
        var labelInfo: String!
        var predictConfidence: String!
        myPOSTRequest(){
            json, error in
            if let json = json as? Message{
                receivedData = json
                print(json)
                if json.className?.isEmpty ?? true{
                    DispatchQueue.main.async {
                        self.activityIndicator.stopAnimating()
                        self.label.text = "Opos, I don't know this mushroom :("
                        
                    }
                    return
                }
                labelInfo = json.className
                var commonName = mushwiki[labelInfo]["common name"]
                predictConfidence = json.classProb
                let floatConfience = Float(predictConfidence)
                let formatedConfidence = String(format: "Similarity: %.2f", floatConfience! * 100)
                var boxes: Array<Array<Float>>!
                print(json)
                DispatchQueue.main.async() {
                    if self.httpResponse == 200{
                        self.label.text = commonName.stringValue
                        self.activityIndicator.stopAnimating()
                        boxes = json.boxes
                        self.handleBoxes(boundaries: boxes)
                        self.confidence.text = "\(formatedConfidence)%"
                        self.readMore.isHidden = false
                        self.confidence.isHidden = false
                        
                    }
                    if self.httpResponse == 500{
                        self.activityIndicator.stopAnimating()
                        self.label.text = "HTTP 500 Error"
                    }
                    if self.httpResponse == 400{
                        return
                    }
                }
                
            }
        }
    }
    
    
}

