//
//  MushroomIntro.swift
//  urlRequest
//
//  Created by Haotian Zhu on 26/5/19.
//  Copyright © 2019 Haotian Zhu. All rights reserved.
//

import UIKit
import SwiftyJSON


class MushroomIntro: UIViewController, UITableViewDelegate, UITableViewDataSource {

    
    @IBOutlet var mushroomName: UILabel!
    @IBOutlet weak var mushroomImage: UIImageView!
    
    var mushroomType: String = ""
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        mushroomType = receivedData.className!
        print("mushroom type is \(mushroomType)")
        mushroomImage.image = getMushroomImage(type: mushroomType)
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        mushroomType = receivedData.className!
        mushroomName.text = mushroomType
        let num : Int = mushwiki[mushroomType]["feature"].array!.count
        print("num of rows " + String(num))
        return num
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = UITableViewCell(style: UITableViewCell.CellStyle.default, reuseIdentifier: "cell")
        cell.textLabel?.text = mushwiki[mushroomType]["feature"][indexPath.row].stringValue
        print("cell value")
        return cell
    }
    
    func getMushroomImage(type: String) -> UIImage{
        var image:UIImage!
        switch type {
        case "button mushroom":
            image = UIImage(named: "button mushroom.jpeg")
        
        case "death cap":
            image = UIImage(named: "death cap.jpg")
        
        case "earthball mushroom":
            image = UIImage(named: "earthball mushroom.jpg")
            
        case "ghost fungus":
            image = UIImage(named: "ghost fungus.jpg")
            
        case "green-spored parasol":
            image = UIImage(named: "green-spored parasol.jpg")
        
        case "haymakers mushroom":
            image = UIImage(named: "haymakers mushroom.jpg")
        
        case "king oyster mushroom":
            image = UIImage(named: "king oyster mushroom.jpeg")
        
        case "pleurotus ostreatus":
            image = UIImage(named: "pleurotus ostreatus.jpg")
        
        case "shaggy parasol":
            image = UIImage(named: "shaggy parasol.jpg")
            
        case "shimeji mushroom":
            image = UIImage(named: "shimeji mushroom.jpg")
            
        case "yellow-staining mushroom":
            image = UIImage(named: "yellow-staining mushroom.jpg")
            
        case "slippery jack":
            image = UIImage(named: "slippery jack.jpg")
            
        default:
            print("No image")
        }
        
        return image
    }

}
