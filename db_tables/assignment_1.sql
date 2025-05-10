-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 10, 2025 at 02:03 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `oop`
--

-- --------------------------------------------------------

--
-- Table structure for table `assignment_1`
--

CREATE TABLE `assignment_1` (
  `id` int(11) NOT NULL,
  `question` text NOT NULL,
  `answer` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `assignment_1`
--

INSERT INTO `assignment_1` (`id`, `question`, `answer`) VALUES
(1, 'What is Object-Oriented Programming (OOP)?', 'Object-Oriented Programming (OOP) is a programming paradigm centered around the concept of \"objects,\" which are instances of classes. It allows developers to structure code in a more modular, reusable, and logical way by representing real-world entities.\r\nKey features of OOP include:\r\n\r\nEncapsulation: Bundling data and methods into one unit (class).\r\n\r\nInheritance: Creating new classes based on existing ones, promoting code reuse.\r\n\r\nPolymorphism: Enabling methods to behave differently based on context.\r\n\r\nAbstraction: Hiding complex implementation details and showing only essential functionalities.\r\nOOP improves code maintainability, readability, and scalability, making it ideal for large and complex software systems.'),
(2, 'What are classes and objects in OOP?', 'In OOP, a class is a user-defined blueprint or template that defines the structure and behavior (attributes and methods) of an object. It acts as a mold for creating objects with similar properties.\r\nAn object is an actual instance of a class, representing a specific entity with unique values. It holds data (attributes) and can perform tasks (methods) defined by its class.'),
(3, 'What is encapsulation?', 'Encapsulation is an OOP principle that combines data and behavior into a single unit — typically a class — while restricting direct access to some parts. It ensures data integrity by making fields private and exposing them through public methods (getters and setters).\r\nBenefits of encapsulation include:\r\n\r\nProtecting internal data from unauthorized access.\r\n\r\nImproving code maintainability and flexibility.\r\neg: class Person {\r\n    private String name;\r\n    private int age;\r\n\r\n    public String getName() {\r\n        return name;\r\n    }\r\n\r\n    public void setName(String newName) {\r\n        name = newName;\r\n    }\r\n}\r\n\r\n\r\nAllowing controlled modification of data.'),
(4, 'What is Inheritance?', 'Inheritance is a fundamental OOP concept that allows a class (subclass) to inherit attributes and methods from another class (superclass). This promotes code reusability, hierarchical relationships, and modular design.\r\n\r\nThere are different types of inheritance:\r\n\r\nSingle Inheritance: A child class inherits from one parent class.\r\n\r\nMultilevel Inheritance: A class inherits from another derived class.\r\n\r\nHierarchical Inheritance: Multiple child classes inherit from one parent class.\r\n\r\nMultiple Inheritance: Not directly supported in Java but achieved using interfaces.\r\n\r\nInheritance helps reduce redundancy, making the code easier to maintain and extend.'),
(5, 'What is Polymorphism?\r\n', 'Polymorphism is the ability of an entity (method, object) to take multiple forms. It enhances code flexibility, maintainability, and reusability by allowing methods to behave differently based on context.\r\n\r\nThere are two main types:\r\n\r\nCompile-time polymorphism (Method Overloading): Multiple methods share the same name but have different parameters.\r\n\r\nRun-time polymorphism (Method Overriding): A subclass redefines a method from its superclass, ensuring dynamic method resolution.\r\n\r\nPolymorphism simplifies code and allows extensions without modifying existing implementations.\r\n\r\n'),
(6, 'What are Constructors in OOP?', 'A constructor is a special method used to initialize objects when they are created. It has the same name as the class and runs automatically during object creation.\r\n\r\nTypes of constructors:\r\n\r\nDefault Constructor: Initializes objects with default values.\r\n\r\nParameterized Constructor: Accepts arguments to set specific values.\r\n\r\nCopy Constructor: Creates a new object by copying an existing object’s properties.\r\n\r\nConstructors improve code efficiency by ensuring that objects start in a valid state.'),
(7, 'What is Method Overloading and Method Overriding?', 'Both method overloading and method overriding allow methods to have the same name but differ in implementation, supporting polymorphism and improving code reusability.\r\n\r\nMethod Overloading (Compile-time Polymorphism):\r\n\r\nOccurs within the same class.\r\n\r\nMethods have the same name but different parameters.\r\n\r\nImproves code readability by handling multiple use cases.\r\n\r\nMethod Overriding (Run-time Polymorphism):\r\n\r\nA subclass redefines a method from its superclass.\r\n\r\nThe overridden method in the child class must have the same signature as in the parent class.\r\n\r\nSupports dynamic method binding and enhances code customization.\r\n\r\nThese features make OOP-based applications more scalable and adaptable.'),
(8, 'What is abstraction?', 'Abstraction simplifies complex systems by focusing on what an object does instead of how it does it. It hides internal details and exposes only relevant functionalities. This can be achieved in two ways:\r\n\r\nAbstract Classes: Defined with the abstract keyword, they can have both abstract (no implementation) and concrete (implemented) methods.\r\n\r\nInterfaces: Define a contract of methods that a class must implement.'),
(9, 'What are Access Modifiers in Java OOP?', 'Access modifiers define the visibility and access control of class members. Java provides four access levels:\r\n\r\nPublic: Accessible from anywhere.\r\n\r\nPrivate: Restricted to the same class.\r\n\r\nProtected: Accessible within the same package and subclasses.\r\n\r\nDefault (Package-private): Accessible within the same package only.\r\n\r\nThese modifiers enforce data security, encapsulation, and proper information hiding, ensuring controlled access to class members.'),
(10, 'What is a Constructor? How is it different from a Method?', 'A constructor is a special method that is called automatically when an object is created. It initializes the object’s state. It has the same name as the class and no return type.\r\nExample:\r\nclass Car {\r\n    String model;\r\n\r\n    Car() {  // Constructor\r\n        model = \"Default Car\";\r\n    }\r\n}\r\nConstructor vs Method:\r\n\r\nFeature	Constructor	Method\r\nPurpose	Initializes an object	Performs an operation\r\nName	Same as class name	Any valid method name\r\nReturn Type	No return type	Must specify return type\r\nInvocation	Called automatically on object creation	Called manually\r\n');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `assignment_1`
--
ALTER TABLE `assignment_1`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `assignment_1`
--
ALTER TABLE `assignment_1`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
