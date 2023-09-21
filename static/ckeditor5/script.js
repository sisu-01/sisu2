ClassicEditor
	.create( document.querySelector( '#editor' ), {
		simpleUpload: {
			uploadUrl: "/upload/image",
			withCredentials: true,
		}
	} )
	.then( editor => {
		window.editor = editor;
		console.log(window.editor);
	} )
	.catch( handleSampleError );

function handleSampleError( error ) {
	const issueUrl = 'https://github.com/ckeditor/ckeditor5/issues';

	const message = [
		'Oops, something went wrong!',
		`Please, report the following error on ${ issueUrl } with the build id "edsteai8845-ktylh53u5b3o" and the error stack trace:`
	].join( '\n' );

	console.error( message );
	console.error( error );
}
