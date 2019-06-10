//
//  imageRotator.swift
//  urlRequest
//
//  Created by Haotian Zhu on 2/6/19.
//  Copyright © 2019 Haotian Zhu. All rights reserved.
//

import UIKit

extension UIImage {
    
    public func imageRotatedByDegrees(degrees: CGFloat) -> UIImage {
        let rotatedSize: CGSize = CGRect(x: 0, y: 0, width: self.size.height, height: self.size.width).size
        
        //Create the bitmap context
        UIGraphicsBeginImageContext(rotatedSize)
        let bitmap: CGContext = UIGraphicsGetCurrentContext()!
        //Move the origin to the middle of the image so we will rotate and scale around the center.
        bitmap.translateBy(x: rotatedSize.width / 2, y: rotatedSize.height / 2)
        //Rotate the image context
        bitmap.rotate(by: (degrees * CGFloat.pi / 180))
        //Now, draw the rotated/scaled image into the context
        bitmap.scaleBy(x: 1.0, y: -1.0)
        bitmap.draw(self.cgImage!, in: CGRect(x: -self.size.width / 2, y: -self.size.height / 2, width: self.size.width, height: self.size.height))
        
        let newImage: UIImage = UIGraphicsGetImageFromCurrentImageContext()!
        
        UIGraphicsEndImageContext()
        return newImage
    }
}
